import pytest
from allie_sdk.methods.group import *


class TestGroupModels:

    def test_group_model(self):
        
        # Expected input
        input = {
            "display_name": "Stewards",
            "email": "stewards@mycompany.com",
            "id": 10,
            "profile_id": 10,
            "url": "/group/10/"
        }

        # Transformation
        input_transformed = Group(**input)

        # Expected Output
        output = Group(
            display_name = "Stewards"
            , email = "stewards@mycompany.com"
            , id = 10
            , profile_id = 10
            , url = "/group/10/"
        )
        

        assert input_transformed == output