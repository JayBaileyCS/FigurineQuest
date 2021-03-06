import copy
import unittest

from game import Commands, Constants, Item, Player, Room
from game.content import Test_Objects


class TestCommands(unittest.TestCase):
    def test_move_command_valid_move(self):
        user_input = "north"
        player = copy.copy(Test_Objects.TEST_PLAYER)
        room = copy.copy(Test_Objects.TEST_ROOM)
        room_two = copy.copy(Test_Objects.TEST_ROOM_2)
        self.assertEqual(player.location.desc, room.desc)
        Commands.parse_move_command(user_input, player)
        self.assertEqual(player.location.desc, room_two.desc)

    def test_move_command_invalid_move(self):
        user_input = "west"
        player = copy.copy(Test_Objects.TEST_PLAYER)
        room = copy.copy(Test_Objects.TEST_ROOM)
        self.assertEqual(player.location.desc, room.desc)
        actual = Commands.parse_move_command(user_input, player)
        self.assertEqual(Constants.EXIT_NOT_FOUND_STRING, actual)

    def test_help_command(self):
        actual = Commands.parse_help_command()
        self.assertEqual(Constants.PLAYER_HELP, actual)

    def test_quit_command(self):
        self.assertEqual(True, True)
        # TODO: Add this

    def test_look_command(self):
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_look_command(player)
        self.assertEqual(player.location.desc, actual)

    def test_examine_command_item_in_room(self):
        user_input = ["examine", "test 2"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_examine_command(user_input, player)
        self.assertEqual(Test_Objects.TEST_ITEM_ON_GROUND.long_desc, actual)

    def test_examine_command_with_keyword(self):
        user_input = ["examine", "keyword"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_examine_command(user_input, player)
        self.assertEqual(Test_Objects.TEST_ITEM_ON_GROUND.long_desc, actual)

    def test_examine_command_item_in_inventory(self):
        user_input = ["examine", "test"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_examine_command(user_input, player)
        self.assertEqual(Test_Objects.TEST_ITEM_IN_INVENTORY.long_desc, actual)

    def test_examine_command_item_not_found(self):
        user_input = ["examine", "test not present"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        expected = Constants.ITEM_NOT_VISIBLE_STRING + "test not present."
        actual = Commands.parse_examine_command(user_input, player)
        self.assertEqual(expected, actual)

    def test_take_command_item_in_room(self):
        user_input = ["take", "test 2"]
        item = Item.Item("test 2", ["keyword"], "Short desc 2", "Long desc 2", True, True)
        room = Room.Room("Test Room", "This is a test room for testing.", {}, [item], [])
        player = Player.Player(room, [Test_Objects.TEST_ITEM_IN_INVENTORY])

        self.assertTrue(item in room.items)
        self.assertTrue(item not in player.inventory)

        actual = Commands.parse_take_command(user_input, player)
        self.assertTrue(item not in room.items)
        self.assertTrue(item in player.inventory)
        self.assertEqual("You take the test 2.", actual)

    def test_take_command_item_with_keyword(self):
        user_input = ["take", "keyword"]
        item = Item.Item("test 2", ["keyword"], "Short desc 2", "Long desc 2", True, True)
        room = Room.Room("Test Room", "This is a test room for testing.", {}, [item], [])
        player = Player.Player(room, [Test_Objects.TEST_ITEM_IN_INVENTORY])

        self.assertTrue(item in room.items)
        self.assertTrue(item not in player.inventory)

        actual = Commands.parse_take_command(user_input, player)
        self.assertTrue(item not in room.items)
        self.assertTrue(item in player.inventory)
        self.assertEqual("You take the test 2.", actual)

    def test_take_command_item_not_present(self):
        user_input = ["take", "test not present"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        room = Room.Room("Test Room", "This is a test room for testing.", {}, [Test_Objects.TEST_ITEM_ON_GROUND], [])
        item = copy.copy(Test_Objects.TEST_ITEM_NOT_PRESENT)

        self.assertTrue(item not in room.items)
        self.assertTrue(item not in player.inventory)

        actual = Commands.parse_take_command(user_input, player)
        self.assertTrue(item not in room.items)
        self.assertTrue(item not in player.inventory)
        self.assertEqual(Constants.ITEM_NOT_VISIBLE_STRING, actual)

    def test_talk_command_person_present(self):
        user_input = ["talk", "testman"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_PERSON_ROOM)
        actual = Commands.parse_talk_command(user_input, player)
        self.assertEqual(Constants.BASE_DIALOGUE, actual)

    def test_talk_command_person_invisible(self):
        user_input = ["talk", "testman"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_INVISIBLE_PERSON_ROOM)
        actual = Commands.parse_talk_command(user_input, player)
        self.assertEqual(Constants.BASE_DIALOGUE, actual)

    def test_talk_command_person_not_present(self):
        user_input = ["talk", "testman"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_talk_command(user_input, player)
        self.assertEqual(Constants.PERSON_NOT_VISIBLE_STRING, actual)

    def test_give_command_valid_command(self):
        user_input = ["give", "testman", "test"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_PERSON_ROOM)
        actual = Commands.parse_give_command(user_input, player)
        self.assertEqual(Constants.INCORRECT_GIFT, actual)

    def test_give_command_with_keyword(self):
        user_input = ["give", "testman", "keyword"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_PERSON_ROOM)
        actual = Commands.parse_give_command(user_input, player)
        self.assertEqual(Constants.INCORRECT_GIFT, actual)

    def test_give_command_person_invisible(self):
        user_input = ["give", "testman", "test"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_INVISIBLE_PERSON_ROOM)
        actual = Commands.parse_give_command(user_input, player)
        expected = Constants.PERSON_NOT_VISIBLE_STRING + "testman."
        self.assertEqual(expected, actual)

    def test_give_command_person_not_present(self):
        user_input = ["give", "testman", "test"]
        player = copy.copy(Test_Objects.TEST_PLAYER)
        actual = Commands.parse_give_command(user_input, player)
        expected = Constants.PERSON_NOT_VISIBLE_STRING + "testman."
        self.assertEqual(expected, actual)

    def test_give_command_item_not_in_inventory(self):
        user_input = ["give", "testman", "test not present"]
        player = copy.copy(Test_Objects.TEST_PLAYER_IN_INVISIBLE_PERSON_ROOM)
        actual = Commands.parse_give_command(user_input, player)
        expected = Constants.ITEM_NOT_IN_INVENTORY_STRING + "test not present."
        self.assertEqual(expected, actual)
