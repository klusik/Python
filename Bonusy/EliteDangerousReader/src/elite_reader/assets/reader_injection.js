/**
 * Elite Dangerous Reader page injection.
 *
 * The script creates an isolated Shadow DOM control panel, applies validated
 * readability CSS, implements the visual element picker, and blocks normal
 * page interactions that attempt top-level navigation outside the approved
 * Elite Dangerous domain. Native WebView2 navigation enforcement remains in
 * the Python layer.
 */
(() => {
    "use strict";

    const INITIAL_SETTINGS = __INITIAL_SETTINGS_JSON__;
    const HOME_URL = __HOME_URL_JSON__;
    const ALLOWED_BASE_DOMAIN = __ALLOWED_BASE_DOMAIN_JSON__;
    const APP_VERSION = __APP_VERSION_JSON__;
    const HOST_ID = "elite-reader-host";
    const STYLE_ID = "elite-reader-page-style";
    const PICKER_STYLE_ID = "elite-reader-picker-style";

    const existingController = window.__eliteDangerousReaderController;
    if (existingController && typeof existingController.reinitialize === "function") {
        existingController.reinitialize(INITIAL_SETTINGS);
        return;
    }

    const state = {
        settings: { ...INITIAL_SETTINGS },
        highlightedElement: null,
        highlightedOutline: "",
        pickerActive: false,
        pywebviewReady: Boolean(window.pywebview && window.pywebview.api),
    };

    function isAllowedUrl(url) {
        try {
            const parsed = new URL(url, window.location.href);
            const host = parsed.hostname.toLowerCase().replace(/\.$/, "");
            return parsed.protocol === "https:" &&
                (host === ALLOWED_BASE_DOMAIN || host.endsWith(`.${ALLOWED_BASE_DOMAIN}`));
        } catch (_error) {
            return false;
        }
    }

    function cssEscape(value) {
        if (window.CSS && typeof window.CSS.escape === "function") {
            return window.CSS.escape(String(value));
        }
        return String(value).replace(/([^a-zA-Z0-9_-])/g, "\\$1");
    }

    function attributeEscape(value) {
        return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
    }

    function createStableSelector(element) {
        if (!(element instanceof Element)) {
            return "body";
        }

        if (element.id) {
            return `#${cssEscape(element.id)}`;
        }

        const stableAttributes = ["data-testid", "data-test", "data-role", "role", "aria-label"];
        for (const attribute of stableAttributes) {
            const value = element.getAttribute(attribute);
            if (value) {
                return `${element.tagName.toLowerCase()}[${attribute}="${attributeEscape(value)}"]`;
            }
        }

        const classes = Array.from(element.classList)
            .filter((name) => name && !/\d{3,}/.test(name) && name.length < 80)
            .slice(0, 3);
        if (classes.length > 0) {
            const candidate = `${element.tagName.toLowerCase()}.${classes.map(cssEscape).join(".")}`;
            try {
                if (document.querySelectorAll(candidate).length <= 12) {
                    return candidate;
                }
            } catch (_error) {
                // Fall back to a structural path.
            }
        }

        const path = [];
        let current = element;
        while (current && current instanceof Element && current !== document.documentElement) {
            let part = current.tagName.toLowerCase();
            if (current.id) {
                path.unshift(`#${cssEscape(current.id)}`);
                break;
            }

            const parent = current.parentElement;
            if (parent) {
                const sameTagSiblings = Array.from(parent.children).filter(
                    (sibling) => sibling.tagName === current.tagName,
                );
                if (sameTagSiblings.length > 1) {
                    part += `:nth-of-type(${sameTagSiblings.indexOf(current) + 1})`;
                }
            }
            path.unshift(part);
            current = parent;
            if (path.length >= 6) {
                break;
            }
        }
        return path.join(" > ") || "body";
    }

    function validateSelector(selector) {
        const normalized = String(selector || "").trim();
        if (!normalized) {
            throw new Error("The CSS selector cannot be empty.");
        }
        document.querySelector(normalized);
        return normalized;
    }

    function buildPageCss(settings) {
        const selector = validateSelector(settings.selector);
        const declarations = [
            `background-color: ${settings.background_color} !important;`,
            `font-size: ${settings.font_scale_percent}% !important;`,
            `line-height: ${settings.line_height} !important;`,
        ];
        if (settings.remove_background_image) {
            declarations.push("background-image: none !important;");
        }

        const rules = [`:is(${selector}) { ${declarations.join(" ")} }`];
        if (settings.text_color) {
            const textTarget = settings.include_descendants_for_text
                ? `:is(${selector}), :is(${selector}) *`
                : `:is(${selector})`;
            rules.push(`${textTarget} { color: ${settings.text_color} !important; }`);
        }
        return rules.join("\n");
    }

    function applyPageStyle(settings, showErrors = true) {
        try {
            let style = document.getElementById(STYLE_ID);
            if (!style) {
                style = document.createElement("style");
                style.id = STYLE_ID;
                (document.head || document.documentElement).appendChild(style);
            }
            style.textContent = buildPageCss(settings);
            state.settings = { ...settings };
            updateControls();
            return true;
        } catch (error) {
            if (showErrors) {
                showStatus(error instanceof Error ? error.message : String(error), true);
            }
            return false;
        }
    }

    function createToolbar() {
        let host = document.getElementById(HOST_ID);
        if (host) {
            return host;
        }

        host = document.createElement("div");
        host.id = HOST_ID;
        host.style.all = "initial";
        host.style.position = "fixed";
        host.style.right = "18px";
        host.style.bottom = "18px";
        host.style.zIndex = "2147483647";
        document.documentElement.appendChild(host);

        const shadow = host.attachShadow({ mode: "open" });
        const style = document.createElement("style");
        style.textContent = `
            :host { all: initial; }
            * { box-sizing: border-box; }
            .launcher, .panel {
                font-family: "Segoe UI", Arial, sans-serif;
                color: #f4f4f4;
            }
            .launcher {
                display: none;
                width: 48px;
                height: 48px;
                border: 1px solid #7b8793;
                border-radius: 50%;
                background: #30343a;
                color: #ffffff;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.45);
                cursor: pointer;
                font-size: 17px;
                font-weight: 700;
            }
            .panel {
                width: 370px;
                max-height: min(720px, calc(100vh - 36px));
                overflow: auto;
                border: 1px solid #68727d;
                border-radius: 10px;
                background: rgba(34, 38, 43, 0.98);
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.52);
            }
            .header {
                position: sticky;
                top: 0;
                z-index: 2;
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 11px 12px;
                border-bottom: 1px solid #555f69;
                background: #292d32;
            }
            .title { flex: 1; min-width: 0; }
            .title strong { display: block; font-size: 14px; }
            .title small { display: block; color: #adb7c0; font-size: 10px; }
            .content { padding: 12px; }
            .nav { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 12px; }
            button, input, label { font: inherit; }
            button {
                border: 1px solid #74808b;
                border-radius: 5px;
                background: #3a4148;
                color: #f4f4f4;
                cursor: pointer;
                min-height: 32px;
                padding: 6px 9px;
            }
            button:hover { background: #4a535c; }
            button.primary { background: #d2691e; border-color: #e47a2a; }
            button.primary:hover { background: #e27627; }
            button.icon { width: 34px; min-height: 30px; padding: 3px; }
            .field { margin-bottom: 11px; }
            .field > label, .label {
                display: block;
                margin-bottom: 5px;
                color: #dce1e6;
                font-size: 11px;
                font-weight: 600;
            }
            .color-row { display: grid; grid-template-columns: 44px 1fr; gap: 7px; }
            input[type="color"] {
                width: 44px;
                height: 34px;
                padding: 2px;
                border: 1px solid #74808b;
                border-radius: 5px;
                background: #25292e;
            }
            input[type="text"], input[type="number"] {
                width: 100%;
                height: 34px;
                padding: 6px 8px;
                border: 1px solid #74808b;
                border-radius: 5px;
                background: #202429;
                color: #ffffff;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
            input[type="range"] { width: 100%; }
            .range-label { display: flex; justify-content: space-between; }
            .checkbox {
                display: flex;
                align-items: center;
                gap: 7px;
                margin-bottom: 8px;
                color: #e2e6ea;
                font-size: 11px;
            }
            .selector-actions { display: grid; grid-template-columns: 1fr auto; gap: 7px; }
            .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-top: 12px; }
            .status {
                min-height: 30px;
                margin-top: 10px;
                padding: 7px 8px;
                border-radius: 5px;
                background: #1e2720;
                color: #a9e5b0;
                font-size: 10px;
                line-height: 1.4;
                overflow-wrap: anywhere;
            }
            .status.error { background: #321f22; color: #ffb3bc; }
            .url {
                margin-bottom: 10px;
                color: #aeb7c0;
                font: 10px/1.4 Consolas, monospace;
                overflow-wrap: anywhere;
            }
            .hint { margin: 4px 0 0; color: #9fa9b3; font-size: 10px; line-height: 1.4; }
            .hidden { display: none !important; }
        `;
        shadow.appendChild(style);

        const launcher = document.createElement("button");
        launcher.className = "launcher";
        launcher.type = "button";
        launcher.title = "Open Elite Reader controls";
        launcher.textContent = "Aa";
        shadow.appendChild(launcher);

        const panel = document.createElement("section");
        panel.className = "panel";
        panel.innerHTML = `
            <div class="header">
                <div class="title">
                    <strong>Elite Reader</strong>
                    <small>WebView2 reader ${APP_VERSION}</small>
                </div>
                <button type="button" class="icon" data-action="collapse" title="Collapse">×</button>
            </div>
            <div class="content">
                <div class="nav">
                    <button type="button" data-action="back" title="Back">←</button>
                    <button type="button" data-action="forward" title="Forward">→</button>
                    <button type="button" data-action="reload" title="Reload">↻</button>
                    <button type="button" data-action="home" title="Update notes home">⌂</button>
                </div>
                <div class="url" data-role="url"></div>
                <div class="field">
                    <span class="label">Background color</span>
                    <div class="color-row">
                        <input type="color" data-role="background-color-picker" aria-label="Background color picker">
                        <input type="text" data-role="background-color" maxlength="7" spellcheck="false">
                    </div>
                </div>
                <div class="field">
                    <span class="label">Optional text color</span>
                    <div class="color-row">
                        <input type="color" data-role="text-color-picker" aria-label="Text color picker">
                        <input type="text" data-role="text-color" maxlength="7" spellcheck="false" placeholder="Empty keeps original text">
                    </div>
                </div>
                <div class="field">
                    <label for="elite-reader-selector">Background element CSS selector</label>
                    <div class="selector-actions">
                        <input id="elite-reader-selector" type="text" data-role="selector" spellcheck="false">
                        <button type="button" data-action="pick">Pick area</button>
                    </div>
                    <p class="hint">Pick the black page area, then click it. The selector is saved.</p>
                </div>
                <label class="checkbox">
                    <input type="checkbox" data-role="remove-image">
                    Remove the selected element's background image
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-role="include-descendants">
                    Apply optional text color to child elements
                </label>
                <div class="field">
                    <div class="range-label label"><span>Font scale</span><span data-role="font-scale-value"></span></div>
                    <input type="range" min="75" max="180" step="5" data-role="font-scale">
                </div>
                <div class="field">
                    <div class="range-label label"><span>Line height</span><span data-role="line-height-value"></span></div>
                    <input type="range" min="1" max="2.5" step="0.05" data-role="line-height">
                </div>
                <div class="actions">
                    <button type="button" class="primary" data-action="apply">Apply and save</button>
                    <button type="button" data-action="reset">Reset defaults</button>
                </div>
                <div class="status" data-role="status">Ready.</div>
            </div>
        `;
        shadow.appendChild(panel);

        const controls = {
            host,
            shadow,
            launcher,
            panel,
            url: shadow.querySelector('[data-role="url"]'),
            status: shadow.querySelector('[data-role="status"]'),
            backgroundColorPicker: shadow.querySelector('[data-role="background-color-picker"]'),
            backgroundColor: shadow.querySelector('[data-role="background-color"]'),
            textColorPicker: shadow.querySelector('[data-role="text-color-picker"]'),
            textColor: shadow.querySelector('[data-role="text-color"]'),
            selector: shadow.querySelector('[data-role="selector"]'),
            removeImage: shadow.querySelector('[data-role="remove-image"]'),
            includeDescendants: shadow.querySelector('[data-role="include-descendants"]'),
            fontScale: shadow.querySelector('[data-role="font-scale"]'),
            fontScaleValue: shadow.querySelector('[data-role="font-scale-value"]'),
            lineHeight: shadow.querySelector('[data-role="line-height"]'),
            lineHeightValue: shadow.querySelector('[data-role="line-height-value"]'),
        };
        state.controls = controls;

        shadow.addEventListener("click", (event) => {
            const button = event.target.closest("button[data-action]");
            if (!button) {
                return;
            }
            const action = button.dataset.action;
            if (action === "back") {
                history.back();
            } else if (action === "forward") {
                history.forward();
            } else if (action === "reload") {
                location.reload();
            } else if (action === "home") {
                location.href = HOME_URL;
            } else if (action === "collapse") {
                setPanelCollapsed(true, true);
            } else if (action === "pick") {
                startPicker();
            } else if (action === "apply") {
                saveFromControls();
            } else if (action === "reset") {
                resetSettings();
            }
        });

        launcher.addEventListener("click", () => setPanelCollapsed(false, true));
        controls.backgroundColorPicker.addEventListener("input", () => {
            controls.backgroundColor.value = controls.backgroundColorPicker.value;
            previewFromControls();
        });
        controls.textColorPicker.addEventListener("input", () => {
            controls.textColor.value = controls.textColorPicker.value;
            previewFromControls();
        });
        controls.fontScale.addEventListener("input", () => {
            controls.fontScaleValue.textContent = `${controls.fontScale.value}%`;
            previewFromControls();
        });
        controls.lineHeight.addEventListener("input", () => {
            controls.lineHeightValue.textContent = Number(controls.lineHeight.value).toFixed(2);
            previewFromControls();
        });
        controls.removeImage.addEventListener("change", previewFromControls);
        controls.includeDescendants.addEventListener("change", previewFromControls);

        return host;
    }

    function controlsToSettings() {
        const controls = state.controls;
        return {
            background_color: controls.backgroundColor.value.trim().toLowerCase(),
            text_color: controls.textColor.value.trim().toLowerCase(),
            selector: controls.selector.value.trim(),
            remove_background_image: controls.removeImage.checked,
            include_descendants_for_text: controls.includeDescendants.checked,
            font_scale_percent: Number.parseInt(controls.fontScale.value, 10),
            line_height: Number.parseFloat(controls.lineHeight.value),
            panel_collapsed: state.settings.panel_collapsed,
        };
    }

    function updateControls() {
        if (!state.controls) {
            return;
        }
        const settings = state.settings;
        const controls = state.controls;
        controls.url.textContent = window.location.href;
        controls.backgroundColor.value = settings.background_color;
        controls.backgroundColorPicker.value = settings.background_color;
        controls.textColor.value = settings.text_color;
        controls.textColorPicker.value = settings.text_color || "#f2f2f2";
        controls.selector.value = settings.selector;
        controls.removeImage.checked = settings.remove_background_image;
        controls.includeDescendants.checked = settings.include_descendants_for_text;
        controls.fontScale.value = String(settings.font_scale_percent);
        controls.fontScaleValue.textContent = `${settings.font_scale_percent}%`;
        controls.lineHeight.value = String(settings.line_height);
        controls.lineHeightValue.textContent = Number(settings.line_height).toFixed(2);
        setPanelCollapsed(Boolean(settings.panel_collapsed), false);
    }

    function previewFromControls() {
        try {
            const candidate = controlsToSettings();
            if (/^#[0-9a-f]{6}$/i.test(candidate.background_color) &&
                (!candidate.text_color || /^#[0-9a-f]{6}$/i.test(candidate.text_color))) {
                applyPageStyle(candidate, false);
            }
        } catch (_error) {
            // Invalid intermediate input is allowed while the user is typing.
        }
    }

    async function callApi(method, ...args) {
        if (!window.pywebview || !window.pywebview.api ||
            typeof window.pywebview.api[method] !== "function") {
            throw new Error("The Python settings bridge is not ready.");
        }
        return window.pywebview.api[method](...args);
    }

    async function saveFromControls() {
        try {
            const candidate = controlsToSettings();
            if (!applyPageStyle(candidate, true)) {
                return;
            }
            showStatus("Saving settings...");
            const result = await callApi("save_settings", candidate);
            if (!result || !result.ok) {
                throw new Error(result && result.error ? result.error : "Settings were rejected.");
            }
            applyPageStyle(result.settings, false);
            showStatus("Settings saved.");
        } catch (error) {
            showStatus(error instanceof Error ? error.message : String(error), true);
        }
    }

    async function persistPanelState(collapsed) {
        try {
            const candidate = { ...state.settings, panel_collapsed: collapsed };
            const result = await callApi("save_settings", candidate);
            if (result && result.ok) {
                state.settings = { ...result.settings };
            }
        } catch (_error) {
            // Collapsing the toolbar remains functional if persistence is unavailable.
        }
    }

    async function resetSettings() {
        try {
            showStatus("Restoring defaults...");
            const result = await callApi("reset_settings");
            if (!result || !result.ok) {
                throw new Error("Defaults could not be restored.");
            }
            applyPageStyle(result.settings, false);
            showStatus("Defaults restored.");
        } catch (error) {
            showStatus(error instanceof Error ? error.message : String(error), true);
        }
    }

    function setPanelCollapsed(collapsed, persist) {
        if (!state.controls) {
            return;
        }
        state.controls.panel.classList.toggle("hidden", collapsed);
        state.controls.launcher.style.display = collapsed ? "block" : "none";
        state.settings = { ...state.settings, panel_collapsed: collapsed };
        if (persist) {
            void persistPanelState(collapsed);
        }
    }

    function showStatus(message, isError = false) {
        if (!state.controls || !state.controls.status) {
            return;
        }
        state.controls.status.textContent = String(message);
        state.controls.status.classList.toggle("error", isError);
    }

    function restoreHighlightedElement() {
        if (state.highlightedElement) {
            state.highlightedElement.style.outline = state.highlightedOutline;
            state.highlightedElement = null;
            state.highlightedOutline = "";
        }
    }

    function stopPicker(cancelled) {
        if (!state.pickerActive) {
            return;
        }
        state.pickerActive = false;
        restoreHighlightedElement();
        document.removeEventListener("mousemove", pickerMouseMove, true);
        document.removeEventListener("click", pickerClick, true);
        document.removeEventListener("keydown", pickerKeyDown, true);
        document.getElementById(PICKER_STYLE_ID)?.remove();
        showStatus(cancelled ? "Area selection cancelled." : "Area selected.");
    }

    function startPicker() {
        stopPicker(true);
        setPanelCollapsed(true, false);
        state.pickerActive = true;
        const style = document.createElement("style");
        style.id = PICKER_STYLE_ID;
        style.textContent = "* { cursor: crosshair !important; }";
        (document.head || document.documentElement).appendChild(style);
        document.addEventListener("mousemove", pickerMouseMove, true);
        document.addEventListener("click", pickerClick, true);
        document.addEventListener("keydown", pickerKeyDown, true);
        showStatus("Click the page area to recolor. Press Esc to cancel.");
    }

    function pickerMouseMove(event) {
        const target = event.target;
        if (!(target instanceof Element) || target.closest(`#${HOST_ID}`)) {
            return;
        }
        if (target === state.highlightedElement) {
            return;
        }
        restoreHighlightedElement();
        state.highlightedElement = target;
        state.highlightedOutline = target.style.outline;
        target.style.outline = "3px solid #ff8c2b";
    }

    function pickerClick(event) {
        const target = event.target;
        if (!(target instanceof Element) || target.closest(`#${HOST_ID}`)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        const selector = createStableSelector(target);
        stopPicker(false);
        setPanelCollapsed(false, false);
        state.controls.selector.value = selector;
        previewFromControls();
        void saveFromControls();
    }

    function pickerKeyDown(event) {
        if (event.key === "Escape") {
            event.preventDefault();
            stopPicker(true);
            setPanelCollapsed(false, false);
        }
    }

    function installLinkGuard() {
        document.addEventListener("click", (event) => {
            const path = typeof event.composedPath === "function" ? event.composedPath() : [];
            const anchor = path.find((item) => item instanceof HTMLAnchorElement) ||
                (event.target instanceof Element ? event.target.closest("a[href]") : null);
            if (!(anchor instanceof HTMLAnchorElement)) {
                return;
            }

            const targetUrl = anchor.href;
            if (!targetUrl || targetUrl.startsWith("javascript:")) {
                event.preventDefault();
                showStatus("Blocked an unsupported link.", true);
                return;
            }
            if (!isAllowedUrl(targetUrl)) {
                event.preventDefault();
                event.stopPropagation();
                showStatus(`External navigation blocked: ${targetUrl}`, true);
                return;
            }
            if (anchor.target && anchor.target.toLowerCase() !== "_self") {
                event.preventDefault();
                window.location.href = targetUrl;
            }
        }, true);

        const originalOpen = window.open.bind(window);
        window.__eliteReaderOriginalWindowOpen = originalOpen;
        window.open = function guardedWindowOpen(url) {
            const targetUrl = String(url || "");
            if (isAllowedUrl(targetUrl)) {
                window.location.href = new URL(targetUrl, window.location.href).href;
            } else {
                showStatus(`External new window blocked: ${targetUrl}`, true);
            }
            return null;
        };
    }

    function installSelfHealingObserver() {
        const observer = new MutationObserver(() => {
            const style = document.getElementById(STYLE_ID);
            if (!style) {
                applyPageStyle(state.settings, false);
            }
            const host = document.getElementById(HOST_ID);
            if (!host) {
                createToolbar();
                updateControls();
            }
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });
        state.observer = observer;
    }

    function initialize(settings) {
        createToolbar();
        applyPageStyle(settings, false);
        updateControls();
        installLinkGuard();
        installSelfHealingObserver();
        showStatus("Ready. Use Pick area if body is not the visible black background.");
    }

    window.addEventListener("pywebviewready", () => {
        state.pywebviewReady = true;
    }, { once: true });

    window.__eliteDangerousReaderController = {
        reinitialize(settings) {
            applyPageStyle(settings, false);
            updateControls();
        },
    };

    initialize(INITIAL_SETTINGS);
})();
