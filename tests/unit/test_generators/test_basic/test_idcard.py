from datetime import datetime

import pytest

from dataforge.core.factory import GeneratorFactory
from dataforge.core.generator import GeneratorConfig
from dataforge.generators.basic.idcard import IDCardValidator


@pytest.fixture
def idcard_validator() -> IDCardValidator:
    """Provides an instance of the ID card validator."""
    return IDCardValidator()


def test_generate_single_valid_id(
    generator_factory: GeneratorFactory, idcard_validator: IDCardValidator
):
    """Test generating a single, valid ID card number."""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = generator_factory.create_generator(config)
    id_card = generator.generate()
    assert idcard_validator.validate(id_card), f"Generated ID {id_card} should be valid"


def test_generate_batch_valid_ids(
    generator_factory: GeneratorFactory, idcard_validator: IDCardValidator
):
    """Test generating a batch of valid ID card numbers."""
    config = GeneratorConfig(generator_type="idcard", parameters={})
    generator = generator_factory.create_generator(config)
    id_cards = generator.generate_batch(10)
    assert len(id_cards) == 10
    for id_card in id_cards:
        assert idcard_validator.validate(
            id_card
        ), f"Generated ID {id_card} in batch should be valid"


def test_generation_with_region_constraint(generator_factory: GeneratorFactory):
    """Test that the region parameter correctly constrains the generated region code."""
    config = GeneratorConfig(generator_type="idcard", parameters={"region": "上海"})
    generator = generator_factory.create_generator(config)
    id_card = generator.generate()
    region_code = id_card[:6]
    assert region_code.startswith(
        "31"
    ), f"ID {id_card} should have a Shanghai region code"


def test_generation_with_birth_date_range(generator_factory: GeneratorFactory):
    """Test that the birth date is generated within the specified range."""
    config = GeneratorConfig(
        generator_type="idcard",
        parameters={"birth_date_range": ("2010-01-01", "2010-12-31")},
    )
    generator = generator_factory.create_generator(config)
    id_card = generator.generate()
    birth_date_str = id_card[6:14]
    birth_date = datetime.strptime(birth_date_str, "%Y%m%d").date()
    assert birth_date.year == 2010


def test_generation_with_gender_constraint(generator_factory: GeneratorFactory):
    """Test that the gender parameter correctly constrains the sequence number."""
    male_generator = generator_factory.create_generator(
        GeneratorConfig(generator_type="idcard", parameters={"gender": "MALE"})
    )
    female_generator = generator_factory.create_generator(
        GeneratorConfig(generator_type="idcard", parameters={"gender": "FEMALE"})
    )

    male_id = male_generator.generate()
    male_gender_digit = int(male_id[16])
    assert male_gender_digit % 2 == 1, "Male ID gender digit should be odd"

    female_id = female_generator.generate()
    female_gender_digit = int(female_id[16])
    assert female_gender_digit % 2 == 0, "Female ID gender digit should be even"


def test_generate_invalid_id(
    generator_factory: GeneratorFactory, idcard_validator: IDCardValidator
):
    """Test generating an invalid ID when valid=False."""
    generator = generator_factory.create_generator(
        GeneratorConfig(generator_type="idcard", parameters={"valid": False})
    )
    invalid_id = generator.generate()
    assert not idcard_validator.validate(
        invalid_id
    ), f"Generated invalid ID {invalid_id} should not be valid"


def test_validate_method_known_values(idcard_validator: IDCardValidator):
    """Test the validate method with known valid and invalid IDs."""
    valid_id = "440303199410133024"
    assert idcard_validator.validate(valid_id)

    invalid_length = "11010119900307071"
    assert not idcard_validator.validate(invalid_length)

    invalid_checksum = "110101199003070711"
    assert not idcard_validator.validate(invalid_checksum)

    invalid_date = "11010119900230071X"
    assert not idcard_validator.validate(invalid_date)

    invalid_region = "999999199003070710"
    assert not idcard_validator.validate(invalid_region)
