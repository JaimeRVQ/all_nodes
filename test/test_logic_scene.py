import os
import unittest
import tempfile

from all_nodes import constants
from all_nodes.logic.logic_scene import LogicScene
from all_nodes.logic.logic_scene import LogicSceneError
from all_nodes import utils

# -------------------------------- TESTS -------------------------------- #
class LogicSceneTesting(unittest.TestCase):

    DICT_EXAMPLE = {
        "test_people": {"names": ["Fred", "Joe", "Sally"], "surnames": None}
    }

    FIXTURES_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "fixtures"
    )

    def test_logic_scene(self):
        """
        Create nodes in a logic scene
        """
        utils.print_separator("TEST STARTED - " + "test_logic_scene")

        logic_scene = LogicScene()
        logic_scene.add_node_by_name("JsonToDict")
        logic_scene.add_node_by_name("GetDictKey")
        logic_scene.add_node_by_name("GetDictKey")
        logic_scene.add_node_by_name("FailNode")
        self.assertEqual(logic_scene.node_count(), 4)

    def test_run_node_graph_starting_at_node(self):
        utils.print_separator(
            "TEST STARTED - " + "test_run_node_graph_starting_at_node"
        )

        logic_scene = LogicScene()
        n_1 = logic_scene.add_node_by_name("StrInput")
        n_1.set_attribute_value("out_str", "test_people")
        n_2 = logic_scene.add_node_by_name("GetDictKey")
        n_2.set_attribute_value("in_dict", LogicSceneTesting.DICT_EXAMPLE)
        n_2["key"].connect_to_other(n_1["out_str"])
        n_3 = logic_scene.add_node_by_name("PrintToConsole")
        n_3["in_object_0"].connect_to_other(n_2["out"])
        n_1._run()
        self.assertTrue(n_1.success)
        self.assertTrue(n_2.success)
        self.assertTrue(n_3.success)

    def test_locate_starting_nodes(self):
        utils.print_separator("TEST STARTED - " + "test_locate_starting_nodes")

        logic_scene = LogicScene()
        logic_scene.add_node_by_name("StrInput")
        n_2 = logic_scene.add_node_by_name("GetDictKey")
        logic_scene.add_node_by_name("PrintToConsole")
        logic_scene.add_node_by_name("CreateTempFile")
        n_5 = logic_scene.add_node_by_name("CreateTempFile")
        n_5[constants.START].connect_to_other(n_2[constants.COMPLETED])
        starting_nodes = logic_scene.get_starting_nodes()
        self.assertEqual(len(starting_nodes), 3)

    def test_capture_node(self):
        utils.print_separator("TEST STARTED - " + "test_capture_node")

        logic_scene = LogicScene()
        n_1 = logic_scene.add_node_by_name("StrInput")
        full_name = n_1.full_name
        n_2 = logic_scene.to_node(full_name)
        self.assertEqual(n_1, n_2)

    def test_write_scene_to_file(self):
        utils.print_separator("TEST STARTED - " + "test_write_scene_to_file")

        logic_scene = LogicScene()
        n_1 = logic_scene.add_node_by_name("StrInput")
        n_1.set_attribute_value("out_str", "TEST")
        n_2 = logic_scene.add_node_by_name("PrintToConsole")
        n_1["out_str"].connect_to_other(n_2["in_object_0"])
        n_2[constants.START].connect_to_other(n_1[constants.COMPLETED])
        logic_scene.run_all_nodes()

        temp = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False)
        temp.close()
        logic_scene.save_to_file(temp.name)
        self.assertTrue(os.path.isfile(temp.name))

    def test_load_scene_from_file(self):
        utils.print_separator("TEST STARTED - " + "test_load_scene_from_file")

        logic_scene = LogicScene()
        logic_scene.load_from_file(
            os.path.join(self.FIXTURES_FOLDER, "environ_to_yaml_and_json.yml")
        )
        self.assertEqual(logic_scene.node_count(), 9)
        # logic_scene.run_all_nodes()  # To be run locally, as it will start files

    def test_load_scene_from_file_2(self):
        utils.print_separator("TEST STARTED - " + "test_load_scene_from_file_2")

        logic_scene = LogicScene()
        with self.assertRaises(LogicSceneError) as e:
            logic_scene.load_from_file(
                os.path.join(self.FIXTURES_FOLDER, "faulty_scene.yml")
            )
        print(e.exception)

    def test_load_scene_from_file_3(self):
        utils.print_separator("TEST STARTED - " + "test_load_scene_from_file_3")

        logic_scene = LogicScene()
        with self.assertRaises(LogicSceneError) as e:
            logic_scene.load_from_file(
                os.path.join(self.FIXTURES_FOLDER, "faulty_scene_2.yml")
            )
        print(e.exception)

    def test_load_scene_from_alias(self):
        utils.print_separator("TEST STARTED - " + "test_load_scene_from_alias")

        logic_scene = LogicScene()
        logic_scene.load_from_file("simple_regex")

    def test_load_scene_from_alias_faulty(self):
        utils.print_separator("TEST STARTED - " + "test_load_scene_from_alias_faulty")

        logic_scene = LogicScene()
        with self.assertRaises(LogicSceneError) as e:
            logic_scene.load_from_file("fake_scene")
        print(e.exception)

    def test_rename_node_incorrect(self):
        utils.print_separator("TEST STARTED - " + "test_rename_node_incorrect")

        logic_scene = LogicScene()
        n = logic_scene.add_node_by_name("PrintToConsole")
        result = logic_scene.rename_node(n, "Bad_name_*?")
        self.assertFalse(result)

    def test_rename_node_already_present(self):
        utils.print_separator("TEST STARTED - " + "test_rename_node_already_present")

        logic_scene = LogicScene()
        n_1 = logic_scene.add_node_by_name("PrintToConsole")
        n_2 = logic_scene.add_node_by_name("YamlToDict")
        self.assertFalse(logic_scene.rename_node(n_1, n_2.full_name))


# -------------------------------- MAIN -------------------------------- #
if __name__ == "__main__":
    unittest.main()
