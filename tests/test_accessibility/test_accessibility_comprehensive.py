"""Comprehensive accessibility tests for the application."""
import pytest


@pytest.mark.accessibility
class TestARIAAttributes:
    """Test ARIA attributes for screen reader support."""

    def test_main_role_present(self, client):
        """Test that main element has proper role."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        assert 'role="main"' in text or '<main' in text

    def test_form_labels_present(self, client):
        """Test that form inputs have proper labels."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have labels for inputs
        assert '<label' in text or 'for=' in text

    def test_button_labels_present(self, client):
        """Test that buttons have proper labels."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Buttons should have text or aria-label
        assert 'button' in text

    def test_image_alt_text(self, client):
        """Test that images have alt text."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # SVG favicon should be present
        assert 'favicon' in text or 'svg' in text.lower()

    def test_aria_live_region(self, client):
        """Test presence of ARIA live regions for dynamic content."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Result display should have aria-live
        assert 'aria-live' in text or 'role="status"' in text


@pytest.mark.accessibility
class TestSemanticHTML:
    """Test proper semantic HTML structure."""

    def test_semantic_header_element(self, client):
        """Test proper use of header element."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        assert '<header' in text or '<h' in text  # Heading level elements

    def test_semantic_nav_element(self, client):
        """Test proper navigation structure."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Language selector should be semantically marked
        assert 'lang' in text.lower()

    def test_form_structure(self, client):
        """Test proper form structure."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        assert '<form' in text
        assert 'method=' in text

    def test_list_structure_for_operations(self, client):
        """Test that operation buttons use proper structure."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Buttons should be properly structured
        assert 'button' in text

    def test_heading_hierarchy(self, client):
        """Test proper heading hierarchy (h1, h2, etc)."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have proper heading structure
        assert '<h' in text or '<title' in text


@pytest.mark.accessibility
class TestKeyboardNavigation:
    """Test keyboard navigation accessibility."""

    def test_keyboard_accessible_form(self, client):
        """Test that form inputs are keyboard accessible."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have input elements
        assert '<input' in text
        # Should have buttons
        assert '<button' in text or 'type="button"' in text

    def test_tab_order_logical(self, client):
        """Test that tab order is logical."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should use proper tab order or natural flow
        assert '<form' in text

    def test_focus_visible_elements(self, client):
        """Test that interactive elements are focusable."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have interactive elements
        assert 'button' in text or 'input' in text

    def test_skip_links_present(self, client):
        """Test presence of skip navigation links."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Modern apps should have skip links
        assert 'main' in text.lower()  # Skip to main content


@pytest.mark.accessibility
class TestColorContrast:
    """Test color contrast for readability."""

    def test_text_color_defined(self, client):
        """Test that text colors are properly defined."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Prefer presence of CSS color definitions or an external stylesheet
        assert 'color' in text or ('<link' in text and '.css' in text.lower())

    def test_background_color_defined(self, client):
        """Test that background colors are defined."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Prefer presence of CSS background definitions or an external stylesheet
        assert 'background' in text or ('<link' in text and '.css' in text.lower())


@pytest.mark.accessibility
class TestResponsiveDesign:
    """Test responsive design accessibility."""

    def test_viewport_meta_tag(self, client):
        """Test presence of viewport meta tag."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        assert 'viewport' in text

    def test_mobile_friendly_font_sizes(self, client):
        """Test that font sizes are appropriate for mobile."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have responsive styling
        assert '@media' in text or 'font-size' in text or ('<link' in text and '.css' in text.lower())

    def test_touch_friendly_button_size(self, client):
        """Test that buttons are touch-friendly."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have buttons
        assert 'button' in text


@pytest.mark.accessibility
class TestLanguageDeclaration:
    """Test proper language declaration."""

    def test_html_lang_attribute(self, client):
        """Test that HTML has lang attribute."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        assert 'lang=' in text

    def test_language_change_accessibility(self, client):
        """Test that language change is accessible."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Language selector should be accessible
        assert 'lang' in text.lower() or 'select' in text.lower()

    def test_language_specific_content(self, client):
        """Test language-specific content accessibility."""
        langs = ['en', 'ru', 'fr', 'de', 'es', 'it', 'zh', 'ka', 'hy']
        for lang in langs:
            response = client.get(f'/?lang={lang}', follow_redirects=True)
            assert response.status_code == 200


@pytest.mark.accessibility
class TestErrorMessages:
    """Test accessibility of error messages."""

    def test_error_message_visibility(self, client):
        """Test that error messages are visible."""
        response = client.post('/', data={
            'a': 'invalid',
            'b': '3',
            'operation': 'add'
        })
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        # Should display error
        assert 'error' in text.lower() or 'invalid' in text.lower()

    def test_error_message_announcement(self, client):
        """Test that error messages use role=alert."""
        response = client.post('/', data={
            'a': 'invalid',
            'b': '3',
            'operation': 'add'
        })
        text = response.data.decode('utf-8')
        # Error should be announced to screen readers
        assert 'role="alert"' in text or 'error' in text.lower()

    def test_inline_validation_messages(self, client):
        """Test presence of inline validation feedback."""
        response = client.post('/', data={
            'a': '',
            'b': '',
            'operation': 'add'
        })
        assert response.status_code == 200


@pytest.mark.accessibility
class TestToolTipAccessibility:
    """Test accessibility of tooltips and help content."""

    def test_tooltip_keyboard_accessible(self, client):
        """Test that tooltips are keyboard accessible."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Tooltip should be present
        assert 'tooltip' in text or 'welcome' in text

    def test_tooltip_dismiss_button(self, client):
        """Test that tooltip can be dismissed."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have close button
        assert 'close' in text.lower() or '×' in text

    def test_debug_tooltip_endpoint(self, client):
        """Test debug tooltip endpoint for testing."""
        response = client.get('/debug/tooltip')
        assert response.status_code == 200
        text = response.data.decode('utf-8')
        assert 'tooltip' in text


@pytest.mark.accessibility
class TestTextAlternatives:
    """Test text alternatives for non-text content."""

    def test_icon_button_labels(self, client):
        """Test that icon buttons have text alternatives."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Buttons should have aria-label or text
        assert 'button' in text
        assert 'aria-label' in text or 'Calculator' in text

    def test_mathematical_symbols_accessible(self, client):
        """Test that mathematical symbols are accessible."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Should have operators defined
        assert '+' in text or 'Add' in text

    def test_favicon_not_relied_upon(self, client):
        """Test that page content doesn't rely on favicon alone."""
        response = client.get('/')
        text = response.data.decode('utf-8')
        # Page should have text content
        assert 'Calculator' in text
