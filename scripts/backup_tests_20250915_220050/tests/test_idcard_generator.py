import os
import sys
import unittest
from datetime import date, datetime

# Add project root to path to allow direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataforge.generators.basic.idcard import IDCardGenerator


class TestIDCardGenerator(unittest.TestCase):
    """Tests for the refactored IDCardGenerator"""

    def setUp(self) -> None:
        """Set up a generator for each test."""
        # This generator is created before each test method
        from dataforge.core.generator import GeneratorConfig

        config = GeneratorConfig(generator_type="idcard", parameters={})
        self.generator = IDCardGenerator(config)

    def test_generate_single_valid_id(self) -> None:
        """Test generating a single, valid ID card number."""
        id_card = self.generator.generate_single()
        self.assertTrue(
            self.generator.validate(id_card), f"Generated ID {id_card} should be valid"
        )

    def test_generate_batch_valid_ids(self) -> None:
        """Test generating a batch of valid ID card numbers."""
        id_cards = self.generator.generate_batch(10)
        self.assertEqual(len(id_cards), 10)
        for id_card in id_cards:
            self.assertTrue(
                self.generator.validate(id_card),
                f"Generated ID {id_card} in batch should be valid",
            )

    def test_generation_with_region_constraint(self) -> None:
        """Test that the region parameter correctly constrains the generated region code."""
        from dataforge.core.generator import GeneratorConfig

        config = GeneratorConfig(generator_type="idcard", parameters={"region": "上海"})
        shanghai_generator = IDCardGenerator(config)
        id_card = shanghai_generator.generate_single()
        region_code = id_card[:6]
        # Shanghai codes start with 310
        self.assertTrue(
            region_code.startswith("31"),
            f"ID {id_card} should have a Shanghai region code",
        )

    def test_generation_with_birth_date_range(self) -> None:
        """Test that the birth date is generated within the specified range."""
        from dataforge.core.generator import GeneratorConfig

        config = GeneratorConfig(
            generator_type="idcard",
            parameters={"birth_date_range": ("2010-01-01", "2010-12-31")},
        )
        generator = IDCardGenerator(config)
        id_card = generator.generate_single()
        birth_date_str = id_card[6:14]
        birth_date = datetime.strptime(birth_date_str, "%Y%m%d").date()
        self.assertEqual(birth_date.year, 2010)

    def test_generation_with_gender_constraint(self) -> None:
        """Test that the gender parameter correctly constrains the sequence number."""
        from dataforge.core.generator import GeneratorConfig

        male_generator = IDCardGenerator(
            GeneratorConfig(generator_type="idcard", parameters={"gender": "MALE"})
        )
        female_generator = IDCardGenerator(
            GeneratorConfig(generator_type="idcard", parameters={"gender": "FEMALE"})
        )

        male_id = male_generator.generate_single()
        male_gender_digit = int(male_id[16])
        self.assertIn(
            male_gender_digit, [1, 3, 5, 7, 9], "Male ID gender digit should be odd"
        )

        female_id = female_generator.generate_single()
        female_gender_digit = int(female_id[16])
        self.assertIn(
            female_gender_digit,
            [0, 2, 4, 6, 8],
            "Female ID gender digit should be even",
        )

    def test_generation_with_age_context(self) -> None:
        """Test generating an ID based on an age value from the context."""
        # Test for a 25-year-old
        from dataforge.core.generator import GeneratorConfig

        generator = IDCardGenerator(
            GeneratorConfig(generator_type="idcard", parameters={})
        )
        id_card = generator.generate_single()
        birth_year = int(id_card[6:10])
        current_year = date.today().year
        calculated_age = current_year - birth_year
        self.assertIn(
            calculated_age,
            [25, 26],
            f"Calculated age for ID {id_card} should be around 25",
        )

    def test_generate_invalid_id(self) -> None:
        """Test generating an invalid ID when valid=False."""
        from dataforge.core.generator import GeneratorConfig

        generator = IDCardGenerator(
            GeneratorConfig(generator_type="idcard", parameters={"valid": False})
        )
        invalid_id = generator.generate_single()
        self.assertFalse(
            self.generator.validate(invalid_id),
            f"Generated invalid ID {invalid_id} should not be valid",
        )

    def test_validate_method_known_values(self) -> None:
        """Test the validate method with known valid and invalid IDs."""
        # A known valid ID (example)
        valid_id = "11010119900307071X"
        self.assertTrue(self.generator.validate(valid_id))

        # Invalid length
        invalid_length = "11010119900307071"
        self.assertFalse(self.generator.validate(invalid_length))

        # Invalid checksum
        invalid_checksum = "110101199003070711"
        self.assertFalse(self.generator.validate(invalid_checksum))

        # Invalid date
        invalid_date = "11010119900230071X"
        self.assertFalse(self.generator.validate(invalid_date))
        # Invalid region code (assuming 999999 is not a valid code)
        invalid_region = "999999199003070710"
        # This test depends on the completeness of regions.json.
        # The refactored validator checks against the loaded list.
        self.assertFalse(self.generator.validate(invalid_region))


if __name__ == "__main__":
    unittest.main(verbosity=2)
