from station_fixture import StationTestCase
import groundstation.objects.root_object as root_object


def assert_objects_equal(test, obj, inst1, inst2):
    for member in obj.data_members:
        test.assertEqual(getattr(inst1, member), getattr(inst2, member))


class TestRootObject(StationTestCase):
    def test_reproducable(self):
        # Create a root object by hand
        obj = root_object.RootObject(
                "test_object",
                "richo@psych0tik.net:groundstation/tests",
                "richo@psych0tik.net:groundstation/testcase"
            )
        hand_proto_data = obj.as_object()
        hand_oid = self.station.write(hand_proto_data)

        proto_obj = root_object.RootObject.from_object(hand_proto_data)
        assert_objects_equal(self, root_object.RootObject, proto_obj, obj)

        git_obj = root_object.RootObject.from_object(self.station[hand_oid].data)
        assert_objects_equal(self, root_object.RootObject, proto_obj, git_obj)
