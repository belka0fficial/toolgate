import unittest
from unittest.mock import patch

from toolgate.mcp import toolgate_mcp


class ToolGateMcpTests(unittest.TestCase):
    def test_tool_input_schema_includes_limits_and_approval(self):
        tool = {
            "id": "sample",
            "inputs": [
                {"name": "query", "type": "string", "required": True, "min_length": 2, "max_length": 20},
                {"name": "count", "type": "integer", "minimum": 1, "maximum": 5, "default": 3},
                {"name": "tags", "type": "array", "item_type": "string", "item_pattern": "^[a-z]+$", "unique_items": True},
            ],
        }

        schema = toolgate_mcp._tool_input_schema(tool)

        self.assertEqual("object", schema["type"])
        self.assertEqual(["query"], schema["required"])
        self.assertEqual(2, schema["properties"]["query"]["minLength"])
        self.assertEqual(5, schema["properties"]["count"]["maximum"])
        self.assertEqual(3, schema["properties"]["count"]["default"])
        self.assertEqual("string", schema["properties"]["tags"]["items"]["type"])
        self.assertTrue(schema["properties"]["tags"]["uniqueItems"])
        self.assertIn("approval_request_id", schema["properties"])

    def test_mcp_tool_name_maps_punctuated_ids_to_safe_names(self):
        self.assertEqual(
            "research_search",
            toolgate_mcp._mcp_tool_name("research.search", ["research.search"]),
        )

    @patch("toolgate.mcp.toolgate_mcp._bootstrap")
    @patch("toolgate.mcp.toolgate_mcp.control_plane.list_objects")
    def test_list_tools_uses_active_control_plane_objects(self, list_objects, _bootstrap):
        list_objects.return_value = [{
            "id": "memorygate.context",
            "description": "Read memory through ToolGate",
            "status": "active",
            "inputs": [{"name": "query", "type": "string", "required": True}],
            "authorization": "auto",
        }]

        tools = toolgate_mcp.list_tools()

        self.assertEqual("memorygate_context", tools[0]["name"])
        self.assertIn("ToolGate id: memorygate.context.", tools[0]["description"])
        self.assertEqual("toolgate_request_status", tools[-1]["name"])

    @patch("toolgate.mcp.toolgate_mcp._bootstrap")
    @patch("toolgate.mcp.toolgate_mcp._server_module")
    @patch("toolgate.mcp.toolgate_mcp.control_plane.list_objects")
    def test_invoke_uses_server_execution_path(self, list_objects, server_module, _bootstrap):
        tool = {"id": "memorygate.context", "status": "active", "inputs": []}
        list_objects.return_value = [tool]
        server_module.return_value.invoke_tool.return_value = {"code": "OK", "result": {"ok": True, "result": {"items": []}}}

        result = toolgate_mcp._invoke("memorygate_context", {"approval_request_id": "req-1"})

        self.assertEqual("OK", result["code"])
        server_module.return_value.invoke_tool.assert_called_once_with(
            tool,
            {},
            "Hermes MCP",
            approval_request_id="req-1",
            actor_id="local-mcp",
        )


if __name__ == "__main__":
    unittest.main()
