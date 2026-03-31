"""Tests for the XHTML sanitiser utility."""

import pytest
from usdm_excel.xhtml_sanitiser import sanitise_xhtml


class TestSanitiseXhtml:
    """Tests covering CORE-001069 and CORE-000945 error patterns."""

    # --- Disallowed elements ---

    def test_removes_style_element(self):
        html = '<div><style>.x { color: red; }</style><p>Text</p></div>'
        cleaned, fixes = sanitise_xhtml(html)
        assert "<style>" not in cleaned
        assert "<p>Text</p>" in cleaned
        assert any("<style>" in f for f in fixes)

    def test_removes_script_element(self):
        html = '<div><script>alert(1)</script><p>Text</p></div>'
        cleaned, fixes = sanitise_xhtml(html)
        assert "<script>" not in cleaned
        assert "<p>Text</p>" in cleaned

    # --- Disallowed attributes ---

    def test_removes_ol_type_attribute(self):
        html = '<ol type="a"><li>Item</li></ol>'
        cleaned, fixes = sanitise_xhtml(html)
        assert 'type=' not in cleaned
        assert any("'type'" in f and "<ol>" in f for f in fixes)

    def test_removes_ul_type_attribute(self):
        html = '<ul type="disc"><li>Item</li></ul>'
        cleaned, fixes = sanitise_xhtml(html)
        assert 'type=' not in cleaned
        assert len(fixes) >= 1

    # --- Malformed HTML repair ---

    def test_repairs_unclosed_p_tag(self):
        html = '<ol><li><p>Text without closing p</li></ol>'
        cleaned, fixes = sanitise_xhtml(html)
        assert "</p>" in cleaned
        assert any("Repaired" in f for f in fixes)

    def test_repairs_mismatched_td_tr(self):
        html = '<table><tr><td>cell 1</tr></table>'
        cleaned, fixes = sanitise_xhtml(html)
        assert "</td>" in cleaned
        assert any("Repaired" in f for f in fixes)

    # --- Combined issues ---

    def test_combined_issues(self):
        html = '<ol type="1"><li><style>h1{}</style>More</li></ol>'
        cleaned, fixes = sanitise_xhtml(html)
        assert 'type=' not in cleaned
        assert '<style>' not in cleaned
        assert len(fixes) >= 2

    # --- Pass-through (no changes) ---

    def test_clean_html_unchanged(self):
        html = '<p>Clean HTML</p>'
        cleaned, fixes = sanitise_xhtml(html)
        assert cleaned == html
        assert fixes == []

    def test_empty_string(self):
        cleaned, fixes = sanitise_xhtml("")
        assert cleaned == ""
        assert fixes == []

    def test_none_returns_none(self):
        cleaned, fixes = sanitise_xhtml(None)
        assert cleaned is None
        assert fixes == []

    def test_whitespace_only(self):
        cleaned, fixes = sanitise_xhtml("   ")
        assert cleaned == "   "
        assert fixes == []

    def test_preserves_valid_attributes(self):
        html = '<table class="data" id="t1"><tr><td>cell</td></tr></table>'
        cleaned, fixes = sanitise_xhtml(html)
        assert 'class="data"' in cleaned
        assert 'id="t1"' in cleaned
        assert fixes == []

    def test_plain_text_unchanged(self):
        html = 'Just some plain text with no tags'
        cleaned, fixes = sanitise_xhtml(html)
        assert cleaned == html
        assert fixes == []

    # --- usdm: namespace preservation ---

    def test_usdm_section_tag_preserved(self):
        """usdm: namespaced tags are internal and should not be altered."""
        html = '<usdm:section name="m11-title">'
        cleaned, fixes = sanitise_xhtml(html)
        assert cleaned == html
        assert fixes == []

    def test_usdm_section_in_div_preserved(self):
        html = '<div><usdm:section name="m11-title"></div>'
        cleaned, fixes = sanitise_xhtml(html)
        assert cleaned == html
        assert fixes == []

    def test_usdm_tag_self_closing_preserved(self):
        html = 'Between <usdm:tag name="min_age"/> and <usdm:tag name="max_age"/>'
        cleaned, fixes = sanitise_xhtml(html)
        assert cleaned == html
        assert fixes == []

    def test_usdm_tag_preserved_alongside_fixes(self):
        html = '<ol type="a"><li>Between <usdm:tag name="min"/> and <usdm:tag name="max"/></li></ol>'
        cleaned, fixes = sanitise_xhtml(html)
        assert 'type=' not in cleaned
        assert '<usdm:tag name="min"/>' in cleaned
        assert '<usdm:tag name="max"/>' in cleaned
