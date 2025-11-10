"""
通讯方式生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestCommunicationGenerator:
    """通讯方式生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个通讯方式"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        comm = generator.generate_single()
        
        assert comm is not None
        assert generator.validate(comm)

    def test_generate_batch(self, generator_factory):
        """测试批量生成通讯方式"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        comms = generator.generate_batch(10)
        
        assert len(comms) == 10
        for comm in comms:
            assert comm is not None

    def test_phone_type(self, generator_factory):
        """测试电话类型"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={"type": "phone"}
        )
        generator = generator_factory.create_generator(config)
        comm = generator.generate_single()
        
        # Should be phone number
        if isinstance(comm, str):
            assert len(comm) >= 8
        elif isinstance(comm, dict):
            assert "phone" in comm or "type" in comm

    def test_email_type(self, generator_factory):
        """测试邮箱类型"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={"type": "email"}
        )
        generator = generator_factory.create_generator(config)
        comm = generator.generate_single()
        
        # Should be email
        if isinstance(comm, str):
            assert "@" in comm
        elif isinstance(comm, dict):
            assert "email" in comm or "type" in comm

    def test_social_media_type(self, generator_factory):
        """测试社交媒体类型"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={"type": "social_media"}
        )
        generator = generator_factory.create_generator(config)
        comm = generator.generate_single()
        
        assert comm is not None

    def test_mixed_types(self, generator_factory):
        """测试混合类型"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={"types": ["phone", "email"]}
        )
        generator = generator_factory.create_generator(config)
        comms = generator.generate_batch(20)
        
        # Should have variety
        assert len(comms) == 20

    def test_validation(self, generator_factory):
        """测试通讯方式验证"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Valid communication
        comm = generator.generate_single()
        assert generator.validate(comm)
        
        # Invalid communications
        assert not generator.validate("")
        assert not generator.validate(None)

    def test_with_label(self, generator_factory):
        """测试带标签"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={"include_label": True}
        )
        generator = generator_factory.create_generator(config)
        comm = generator.generate_single()
        
        # May return dict with label
        assert comm is not None

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        from dataforge.generators.contact.communication import CommunicationGenerator
        generator_factory.registry.register("communication", CommunicationGenerator)
        
        config = GeneratorConfig(
            generator_type="communication",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        
        # Generate multiple times
        for _ in range(10):
            comm = generator.generate_single()
            assert comm is not None
