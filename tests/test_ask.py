from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
    )
    request = {}

    def generate_content(**kwargs):
        request.update(kwargs)
        return response

    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=generate_content)
    )
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask, "perf_counter", iter([1.0, 1.25]).__next__)

    assert ask.ask("質問", temperature=0.0) == "回答"
    output = capsys.readouterr().out
    assert request["contents"] == "質問"
    assert request["config"].temperature == 0.0
    assert "[実行時間] 0.25 秒" in output
    assert "[トークン] 入力: 12, 出力: 7" in output


def test_main_runs_all_temperatures_and_prints_each_answer(monkeypatch, capsys):
    requests = []

    def generate_content(**kwargs):
        requests.append(kwargs)
        return SimpleNamespace(text=f"回答 {kwargs['config'].temperature}", usage_metadata=None)

    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=generate_content)
    )
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask, "perf_counter", iter([0, 1, 2, 3, 4, 5]).__next__)
    monkeypatch.setattr("sys.argv", ["app.ask", "共通の質問"])

    ask.main()

    output = capsys.readouterr().out
    assert [request["config"].temperature for request in requests] == [0.0, 0.5, 1.0]
    assert output.count("[実行時間] 1.00 秒") == 3
    assert all(f"回答 {temperature}" in output for temperature in (0.0, 0.5, 1.0))