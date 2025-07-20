from sample_finder.sources.source import Source


class TestSources:
    def test_supported_hash(self) -> None:
        assert not Source.supported_hash("a")
        assert Source.supported_hash("93b885adfe0da089cdf634904fd59f71")
        assert Source.supported_hash("5ba93c9db0cff93f52b521d7420e43f6eda2784f")
        assert Source.supported_hash("fff9292b4201617bdc4d3053fce02734166a683d7d858a7f5f59b073")
        assert Source.supported_hash("6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d")
        assert Source.supported_hash(
            "bec021b4f368e3069134e012c2b4307083d3a9bdd206e24e5f0d86e13d6636655933ec2b413465966817a9c208a11717"
        )
        assert Source.supported_hash(
            "b8244d028981d693af7b456af8efa4cad63d282e19ff14942c246e50d9351d22704a802a71c3580b6370de4ceb293c324a8423342557d4e5c38438f0e36910ee"
        )

    def test_get_source(self) -> None:
        for sc in Source.__subclasses__():
            assert isinstance(sc.NAME, str)
            assert sc.NAME.islower()
            assert isinstance(Source.get_source(sc.NAME, {"api_key": ""}), sc)
