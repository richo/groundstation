from station_fixture import StationTestCase
import groundstation.objects.update_object as update_object


def assert_objects_equal(test, obj, inst1, inst2):
    for member in obj.data_members:
        test.assertEqual(getattr(inst1, member), getattr(inst2, member))


class TestUpdateObject(StationTestCase):
    def test_reproducable(self):
        # Create a root object by hand
        obj = update_object.UpdateObject(
                ["d41e2dadaf624319518a9dfa8ef4cb0dde055b5c",
                 "039727ec5a50d0ed45ff67e6f4c9b953bd23c17d"
                 ],
                "Lol I r update data"
            )
        hand_proto_data = obj.as_object()
        hand_oid = self.station.write(hand_proto_data)

        proto_obj = update_object.UpdateObject.from_object(hand_proto_data)
        assert_objects_equal(self, update_object.UpdateObject, proto_obj, obj)

        git_obj = update_object.UpdateObject.from_object(self.station[hand_oid].data)
        assert_objects_equal(self, update_object.UpdateObject, proto_obj, git_obj)
