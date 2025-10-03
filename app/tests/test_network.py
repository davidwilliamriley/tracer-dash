def test_network_view_creates_layout():
    data = {"elements": []}
    layout = NetworkView.create_layout(data)
    assert layout is not None

def test_js_files_exist():
    js_path = Path('static/js')
    assert (js_path / 'cytoscape_callback.js').exists()
    assert (js_path / 'cytoscape_config.js').exists()
    # ... test other files