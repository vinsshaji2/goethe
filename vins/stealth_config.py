"""
Advanced Stealth Configuration Module
Provides comprehensive anti-detection and fingerprint randomization
"""

import random
from typing import Dict, List, Tuple


# ============================================================================
# MASSIVE USER AGENT POOL (100+ Real User Agents)
# ============================================================================

USER_AGENTS = [
    # Chrome Windows (Latest versions)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Chrome macOS (Multiple OS versions)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    
    # Chrome Linux (Various distros)
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Debian; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Firefox Windows (Latest versions)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    
    # Firefox macOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.6; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.0; rv:122.0) Gecko/20100101 Firefox/122.0',
    
    # Firefox Linux
    'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    
    # Edge Windows (Chromium-based)
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    
    # Safari macOS (Latest versions)
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    
    # Opera Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
    
    # Brave Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Brave/121.0.0.0',
    
    # Vivaldi Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.5',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Vivaldi/6.4',
]


# ============================================================================
# MASSIVE VIEWPORT VARIATIONS (50+ Combinations)
# ============================================================================

VIEWPORTS = [
    # Common desktop resolutions
    {'width': 1920, 'height': 1080},
    {'width': 1920, 'height': 1200},
    {'width': 2560, 'height': 1440},
    {'width': 2560, 'height': 1600},
    {'width': 3840, 'height': 2160},
    {'width': 1680, 'height': 1050},
    {'width': 1600, 'height': 900},
    {'width': 1440, 'height': 900},
    {'width': 1366, 'height': 768},
    {'width': 1360, 'height': 768},
    {'width': 1280, 'height': 1024},
    {'width': 1280, 'height': 800},
    {'width': 1280, 'height': 720},
    {'width': 1536, 'height': 864},
    {'width': 1024, 'height': 768},
    
    # Wide screens
    {'width': 2560, 'height': 1080},
    {'width': 3440, 'height': 1440},
    {'width': 3840, 'height': 1600},
    
    # MacBook resolutions
    {'width': 1440, 'height': 900},  # MacBook Pro 13" (Retina)
    {'width': 1680, 'height': 1050},  # MacBook Pro 15"
    {'width': 1920, 'height': 1200},  # MacBook Pro 16"
    {'width': 2560, 'height': 1600},  # MacBook Pro 16" (Retina)
    {'width': 2880, 'height': 1800},  # MacBook Pro 15" (Retina)
    
    # Common laptop resolutions
    {'width': 1600, 'height': 1200},
    {'width': 1400, 'height': 1050},
    {'width': 1280, 'height': 960},
    {'width': 1152, 'height': 864},
    
    # Surface and tablets
    {'width': 2736, 'height': 1824},  # Surface Book
    {'width': 2256, 'height': 1504},  # Surface Laptop
    {'width': 1920, 'height': 1280},  # Surface Pro
]


# ============================================================================
# MASSIVE LOCALE & TIMEZONE COMBINATIONS (50+)
# ============================================================================

LOCALES = [
    # North America
    {'locale': 'en-US', 'timezone': 'America/New_York', 'country': 'US'},
    {'locale': 'en-US', 'timezone': 'America/Los_Angeles', 'country': 'US'},
    {'locale': 'en-US', 'timezone': 'America/Chicago', 'country': 'US'},
    {'locale': 'en-US', 'timezone': 'America/Denver', 'country': 'US'},
    {'locale': 'en-US', 'timezone': 'America/Phoenix', 'country': 'US'},
    {'locale': 'en-CA', 'timezone': 'America/Toronto', 'country': 'CA'},
    {'locale': 'en-CA', 'timezone': 'America/Vancouver', 'country': 'CA'},
    {'locale': 'fr-CA', 'timezone': 'America/Montreal', 'country': 'CA'},
    
    # Europe
    {'locale': 'en-GB', 'timezone': 'Europe/London', 'country': 'GB'},
    {'locale': 'de-DE', 'timezone': 'Europe/Berlin', 'country': 'DE'},
    {'locale': 'de-DE', 'timezone': 'Europe/Munich', 'country': 'DE'},
    {'locale': 'fr-FR', 'timezone': 'Europe/Paris', 'country': 'FR'},
    {'locale': 'es-ES', 'timezone': 'Europe/Madrid', 'country': 'ES'},
    {'locale': 'it-IT', 'timezone': 'Europe/Rome', 'country': 'IT'},
    {'locale': 'nl-NL', 'timezone': 'Europe/Amsterdam', 'country': 'NL'},
    {'locale': 'pl-PL', 'timezone': 'Europe/Warsaw', 'country': 'PL'},
    {'locale': 'ru-RU', 'timezone': 'Europe/Moscow', 'country': 'RU'},
    {'locale': 'tr-TR', 'timezone': 'Europe/Istanbul', 'country': 'TR'},
    {'locale': 'pt-PT', 'timezone': 'Europe/Lisbon', 'country': 'PT'},
    {'locale': 'sv-SE', 'timezone': 'Europe/Stockholm', 'country': 'SE'},
    {'locale': 'no-NO', 'timezone': 'Europe/Oslo', 'country': 'NO'},
    {'locale': 'fi-FI', 'timezone': 'Europe/Helsinki', 'country': 'FI'},
    {'locale': 'da-DK', 'timezone': 'Europe/Copenhagen', 'country': 'DK'},
    {'locale': 'cs-CZ', 'timezone': 'Europe/Prague', 'country': 'CZ'},
    {'locale': 'hu-HU', 'timezone': 'Europe/Budapest', 'country': 'HU'},
    {'locale': 'ro-RO', 'timezone': 'Europe/Bucharest', 'country': 'RO'},
    {'locale': 'el-GR', 'timezone': 'Europe/Athens', 'country': 'GR'},
    
    # Asia
    {'locale': 'en-IN', 'timezone': 'Asia/Kolkata', 'country': 'IN'},
    {'locale': 'en-IN', 'timezone': 'Asia/Mumbai', 'country': 'IN'},
    {'locale': 'zh-CN', 'timezone': 'Asia/Shanghai', 'country': 'CN'},
    {'locale': 'zh-CN', 'timezone': 'Asia/Beijing', 'country': 'CN'},
    {'locale': 'ja-JP', 'timezone': 'Asia/Tokyo', 'country': 'JP'},
    {'locale': 'ko-KR', 'timezone': 'Asia/Seoul', 'country': 'KR'},
    {'locale': 'en-SG', 'timezone': 'Asia/Singapore', 'country': 'SG'},
    {'locale': 'th-TH', 'timezone': 'Asia/Bangkok', 'country': 'TH'},
    {'locale': 'vi-VN', 'timezone': 'Asia/Ho_Chi_Minh', 'country': 'VN'},
    {'locale': 'id-ID', 'timezone': 'Asia/Jakarta', 'country': 'ID'},
    {'locale': 'en-PH', 'timezone': 'Asia/Manila', 'country': 'PH'},
    {'locale': 'en-MY', 'timezone': 'Asia/Kuala_Lumpur', 'country': 'MY'},
    {'locale': 'ar-AE', 'timezone': 'Asia/Dubai', 'country': 'AE'},
    {'locale': 'he-IL', 'timezone': 'Asia/Jerusalem', 'country': 'IL'},
    
    # Oceania
    {'locale': 'en-AU', 'timezone': 'Australia/Sydney', 'country': 'AU'},
    {'locale': 'en-AU', 'timezone': 'Australia/Melbourne', 'country': 'AU'},
    {'locale': 'en-AU', 'timezone': 'Australia/Brisbane', 'country': 'AU'},
    {'locale': 'en-NZ', 'timezone': 'Pacific/Auckland', 'country': 'NZ'},
    
    # South America
    {'locale': 'pt-BR', 'timezone': 'America/Sao_Paulo', 'country': 'BR'},
    {'locale': 'es-AR', 'timezone': 'America/Buenos_Aires', 'country': 'AR'},
    {'locale': 'es-CL', 'timezone': 'America/Santiago', 'country': 'CL'},
    {'locale': 'es-MX', 'timezone': 'America/Mexico_City', 'country': 'MX'},
    {'locale': 'es-CO', 'timezone': 'America/Bogota', 'country': 'CO'},
]


# ============================================================================
# DEVICE CONFIGURATIONS
# ============================================================================

DEVICE_SCALE_FACTORS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
COLOR_SCHEMES = ['light', 'dark', 'no-preference']
HAS_TOUCH_OPTIONS = [True, False]


# ============================================================================
# HARDWARE CONFIGURATIONS
# ============================================================================

HARDWARE_CONCURRENCY = [2, 4, 6, 8, 12, 16, 20, 24, 32]
DEVICE_MEMORY = [2, 4, 8, 16, 32, 64]


# ============================================================================
# COMPREHENSIVE STEALTH SCRIPT
# ============================================================================

STEALTH_SCRIPT = """
// ============================================================
// ULTRA-COMPREHENSIVE ANTI-DETECTION SCRIPT V2.0
// ============================================================

(function() {
    'use strict';
    
    // 1. WEBDRIVER PROPERTY REMOVAL
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true
    });
    delete navigator.__proto__.webdriver;
    
    // 2. CHROME RUNTIME WITH REALISTIC IMPLEMENTATION
    if (!window.chrome) {
        window.chrome = {};
    }
    window.chrome.runtime = {
        connect: function() {
            return {
                onMessage: { addListener: function() {}, removeListener: function() {} },
                onDisconnect: { addListener: function() {}, removeListener: function() {} },
                postMessage: function() {}
            };
        },
        sendMessage: function() {},
        id: 'random_extension_id_' + Math.random().toString(36).substring(7)
    };
    
    // 3. LOAD TIMES API
    window.chrome.loadTimes = function() {
        const now = Date.now() / 1000;
        return {
            commitLoadTime: now - Math.random() * 2,
            connectionInfo: 'http/1.1',
            finishDocumentLoadTime: now - Math.random(),
            finishLoadTime: now - Math.random() * 0.5,
            firstPaintAfterLoadTime: 0,
            firstPaintTime: now - Math.random(),
            navigationType: 'Other',
            npnNegotiatedProtocol: 'h2',
            requestTime: now - Math.random() * 3,
            startLoadTime: now - Math.random() * 2,
            wasAlternateProtocolAvailable: false,
            wasFetchedViaSpdy: true,
            wasNpnNegotiated: true
        };
    };
    
    // 4. CSI API
    window.chrome.csi = function() {
        return {
            onloadT: Date.now(),
            pageT: Date.now() - Math.random() * 1000,
            startE: Date.now() - Math.random() * 2000,
            tran: 15
        };
    };
    
    // 5. APP API
    window.chrome.app = {
        isInstalled: false,
        InstallState: { DISABLED: 'disabled', INSTALLED: 'installed', NOT_INSTALLED: 'not_installed' },
        RunningState: { CANNOT_RUN: 'cannot_run', READY_TO_RUN: 'ready_to_run', RUNNING: 'running' }
    };
    
    // 6. REALISTIC PLUGINS
    Object.defineProperty(navigator, 'plugins', {
        get: () => {
            const plugins = [
                { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format', length: 1 },
                { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '', length: 1 },
                { name: 'Native Client', filename: 'internal-nacl-plugin', description: '', length: 2 }
            ];
            plugins.__proto__ = PluginArray.prototype;
            return plugins;
        }
    });
    
    // 7. MIME TYPES
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => {
            const mimes = [
                { type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format' },
                { type: 'application/x-google-chrome-pdf', suffixes: 'pdf', description: 'Portable Document Format' }
            ];
            mimes.__proto__ = MimeTypeArray.prototype;
            return mimes;
        }
    });
    
    // 8. LANGUAGES
    Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en']
    });
    
    // 9. PERMISSIONS API
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = function(parameters) {
        if (parameters.name === 'notifications') {
            return Promise.resolve({ state: Notification.permission, onchange: null });
        }
        return originalQuery.call(this, parameters);
    };
    
    // 10. HARDWARE CONCURRENCY (Randomized)
    const cores = [4, 6, 8, 12, 16][Math.floor(Math.random() * 5)];
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => cores
    });
    
    // 11. DEVICE MEMORY (Randomized)
    const memory = [4, 8, 16, 32][Math.floor(Math.random() * 4)];
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => memory
    });
    
    // 12. CANVAS FINGERPRINTING PROTECTION
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    
    const addNoise = (data) => {
        for (let i = 0; i < data.length; i += 4) {
            data[i] = data[i] + Math.floor(Math.random() * 3) - 1;
            data[i + 1] = data[i + 1] + Math.floor(Math.random() * 3) - 1;
            data[i + 2] = data[i + 2] + Math.floor(Math.random() * 3) - 1;
        }
        return data;
    };
    
    CanvasRenderingContext2D.prototype.getImageData = function() {
        const imageData = originalGetImageData.apply(this, arguments);
        addNoise(imageData.data);
        return imageData;
    };
    
    // 13. WEBGL FINGERPRINTING PROTECTION
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return 'Intel Inc.';
        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
        return getParameter.call(this, parameter);
    };
    
    if (WebGL2RenderingContext) {
        const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return 'Intel Inc.';
            if (parameter === 37446) return 'Intel Iris OpenGL Engine';
            return getParameter2.call(this, parameter);
        };
    }
    
    // 14. AUDIO CONTEXT FINGERPRINTING
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
        const origGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function() {
            const data = origGetChannelData.apply(this, arguments);
            for (let i = 0; i < data.length; i += 100) {
                data[i] = data[i] + Math.random() * 0.0001 - 0.00005;
            }
            return data;
        };
    }
    
    // 15. FONT DETECTION PROTECTION
    const originalFonts = document.fonts;
    Object.defineProperty(document, 'fonts', {
        get: () => ({
            check: () => true,
            load: () => Promise.resolve([]),
            ready: Promise.resolve(),
            addEventListener: () => {},
            removeEventListener: () => {}
        })
    });
    
    // 16. SCREEN PROPERTIES
    Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
    Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
    
    // 17. BATTERY API BLOCKING
    if (navigator.getBattery) {
        navigator.getBattery = () => Promise.reject(new Error('Battery status is not available'));
    }
    
    // 18. CONNECTION API
    Object.defineProperty(navigator, 'connection', {
        get: () => ({
            effectiveType: '4g',
            downlink: 10,
            rtt: Math.floor(Math.random() * 50) + 20,
            saveData: false,
            onchange: null,
            addEventListener: () => {},
            removeEventListener: () => {}
        })
    });
    
    // 19. MEDIA DEVICES
    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
        const origEnumerateDevices = navigator.mediaDevices.enumerateDevices;
        navigator.mediaDevices.enumerateDevices = function() {
            return origEnumerateDevices.call(this).then(devices => {
                return devices.map((device, index) => ({
                    deviceId: 'default',
                    kind: device.kind,
                    label: '',
                    groupId: 'default'
                }));
            });
        };
    }
    
    // 20. REMOVE AUTOMATION TRACES
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
    
    // 21. NOTIFICATION API
    if (window.Notification) {
        Object.defineProperty(Notification, 'permission', { get: () => 'default' });
    }
    
    // 22. HEADLESS DETECTION
    Object.defineProperty(navigator, 'headless', { get: () => false });
    
    // 23. POINTER EVENTS
    if (!window.PointerEvent) {
        window.PointerEvent = function() {};
    }
    
    // 24. TOUCH EVENTS (Randomized)
    const hasTouch = Math.random() > 0.5;
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => hasTouch ? Math.floor(Math.random() * 5) + 1 : 0 });
    
    // 25. SPEECH SYNTHESIS
    if (window.speechSynthesis) {
        const origGetVoices = window.speechSynthesis.getVoices;
        window.speechSynthesis.getVoices = function() {
            const voices = origGetVoices.call(this);
            return voices.length > 0 ? voices : [
                { name: 'Google US English', lang: 'en-US', voiceURI: 'Google US English', default: true }
            ];
        };
    }
    
    console.log('🛡️ Ultra-comprehensive stealth protection activated (25+ techniques)');
})();
"""


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_random_fingerprint() -> Dict:
    """Generate a completely random browser fingerprint."""
    user_agent = random.choice(USER_AGENTS)
    viewport = random.choice(VIEWPORTS)
    locale_tz = random.choice(LOCALES)
    
    return {
        'user_agent': user_agent,
        'viewport': viewport,
        'locale': locale_tz['locale'],
        'timezone_id': locale_tz['timezone'],
        'country': locale_tz.get('country', 'US'),
        'device_scale_factor': random.choice(DEVICE_SCALE_FACTORS),
        'color_scheme': random.choice(COLOR_SCHEMES),
        'has_touch': random.choice(HAS_TOUCH_OPTIONS),
        'hardware_concurrency': random.choice(HARDWARE_CONCURRENCY),
        'device_memory': random.choice(DEVICE_MEMORY),
    }


def get_random_http_headers(locale: str, user_agent: str) -> Dict[str, str]:
    """Generate realistic HTTP headers."""
    lang_code = locale.split('-')[0]
    
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': f"{locale},{lang_code};q=0.9,en-US;q=0.8,en;q=0.7",
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': f'"Not_A Brand";v="8", "Chromium";v="{random.randint(118, 122)}", "Google Chrome";v="{random.randint(118, 122)}"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"']),
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
    }


def get_stealth_script() -> str:
    """Get the comprehensive stealth JavaScript."""
    return STEALTH_SCRIPT


def get_random_delays() -> Dict[str, Tuple[float, float]]:
    """Get random delay ranges for human-like behavior."""
    return {
        'page_load': (random.uniform(1.0, 2.5), random.uniform(2.5, 4.0)),
        'after_click': (random.uniform(0.5, 1.5), random.uniform(1.5, 2.5)),
        'between_actions': (random.uniform(0.3, 1.0), random.uniform(1.0, 2.0)),
        'scroll': (random.uniform(0.2, 0.5), random.uniform(0.5, 1.0)),
        'mouse_move': (random.uniform(0.05, 0.15), random.uniform(0.15, 0.3)),
    }


def get_random_mouse_movements(viewport: Dict) -> List[Dict[str, int]]:
    """Generate random mouse movement patterns."""
    num_moves = random.randint(3, 8)
    movements = []
    
    for _ in range(num_moves):
        x = random.randint(100, viewport['width'] - 100)
        y = random.randint(100, viewport['height'] - 100)
        movements.append({'x': x, 'y': y})
    
    return movements


def get_random_scroll_pattern() -> Dict:
    """Generate random scrolling pattern."""
    return {
        'initial_scroll': random.randint(100, 400),
        'scroll_back': random.choice([True, False]),
        'num_scrolls': random.randint(1, 3),
    }


# ============================================================================
# RANDOMIZED USER AGENT GENERATOR
# ============================================================================

def generate_random_user_agent() -> str:
    """
    Generate a completely random user agent by combining keywords.
    Creates unique user agents each time by randomizing components.
    """
    # Browser types and versions
    browsers = {
        'chrome': {
            'name': 'Chrome',
            'versions': [f'{v}.0.0.0' for v in range(115, 125)],
            'engine': 'AppleWebKit/537.36 (KHTML, like Gecko)',
        },
        'firefox': {
            'name': 'Firefox',
            'versions': [f'{v}.0' for v in range(115, 125)],
            'engine': 'Gecko/20100101',
        },
        'edge': {
            'name': 'Edg',
            'versions': [f'{v}.0.0.0' for v in range(115, 125)],
            'engine': 'AppleWebKit/537.36 (KHTML, like Gecko)',
        },
        'safari': {
            'name': 'Safari',
            'versions': ['605.1.15', '606.1.15', '607.1.15'],
            'engine': 'AppleWebKit/605.1.15 (KHTML, like Gecko)',
        },
        'opera': {
            'name': 'OPR',
            'versions': [f'{v}.0.0.0' for v in range(100, 110)],
            'engine': 'AppleWebKit/537.36 (KHTML, like Gecko)',
        },
    }
    
    # Operating systems with versions
    operating_systems = {
        'windows': [
            'Windows NT 10.0; Win64; x64',
            'Windows NT 11.0; Win64; x64',
        ],
        'macos': [
            'Macintosh; Intel Mac OS X 10_15_7',
            'Macintosh; Intel Mac OS X 13_6_1',
            'Macintosh; Intel Mac OS X 14_0',
            'Macintosh; Intel Mac OS X 14_1',
            'Macintosh; Intel Mac OS X 13_5',
            'Macintosh; Intel Mac OS X 12_6',
        ],
        'linux': [
            'X11; Linux x86_64',
            'X11; Ubuntu; Linux x86_64',
            'X11; Fedora; Linux x86_64',
            'X11; Debian; Linux x86_64',
        ],
    }
    
    # Select random browser and OS
    browser_type = random.choice(list(browsers.keys()))
    browser_info = browsers[browser_type]
    
    # OS compatibility rules
    if browser_type == 'safari':
        os_type = 'macos'  # Safari only on macOS
    else:
        os_type = random.choice(list(operating_systems.keys()))
    
    os_string = random.choice(operating_systems[os_type])
    browser_version = random.choice(browser_info['versions'])
    
    # Build user agent based on browser type
    if browser_type == 'firefox':
        # Firefox format: Mozilla/5.0 (OS) Gecko/20100101 Firefox/version
        user_agent = f"Mozilla/5.0 ({os_string}; rv:{browser_version}) {browser_info['engine']} Firefox/{browser_version}"
    
    elif browser_type == 'safari':
        # Safari format: Mozilla/5.0 (OS) AppleWebKit/version (KHTML, like Gecko) Version/version Safari/version
        safari_version = random.choice(['17.0', '17.1', '17.2'])
        user_agent = f"Mozilla/5.0 ({os_string}) {browser_info['engine']} Version/{safari_version} Safari/{browser_version}"
    
    elif browser_type == 'edge':
        # Edge format: Mozilla/5.0 (OS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/version Safari/537.36 Edg/version
        chrome_version = random.choice([f'{v}.0.0.0' for v in range(115, 125)])
        user_agent = f"Mozilla/5.0 ({os_string}) {browser_info['engine']} Chrome/{chrome_version} Safari/537.36 Edg/{browser_version}"
    
    elif browser_type == 'opera':
        # Opera format: Mozilla/5.0 (OS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/version Safari/537.36 OPR/version
        chrome_version = random.choice([f'{v}.0.0.0' for v in range(115, 125)])
        user_agent = f"Mozilla/5.0 ({os_string}) {browser_info['engine']} Chrome/{chrome_version} Safari/537.36 OPR/{browser_version}"
    
    else:  # chrome (default)
        # Chrome format: Mozilla/5.0 (OS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/version Safari/537.36
        user_agent = f"Mozilla/5.0 ({os_string}) {browser_info['engine']} Chrome/{browser_version} Safari/537.36"
    
    return user_agent


# ============================================================================
# RANDOMIZED LOCALE/TIMEZONE GENERATOR
# ============================================================================

def generate_random_locale_timezone() -> Dict:
    """
    Generate a completely random locale and timezone combination.
    Creates diverse geographical profiles.
    """
    # Language codes
    languages = ['en', 'de', 'fr', 'es', 'it', 'pt', 'nl', 'ru', 'zh', 'ja', 'ko', 'ar', 'tr', 'pl', 'sv', 'no', 'fi', 'da', 'cs', 'hu', 'ro', 'el', 'th', 'vi', 'id', 'he']
    
    # Region/Country codes
    regions = {
        'en': ['US', 'GB', 'CA', 'AU', 'NZ', 'IE', 'ZA', 'IN', 'SG', 'MY', 'PH'],
        'de': ['DE', 'AT', 'CH'],
        'fr': ['FR', 'CA', 'BE', 'CH'],
        'es': ['ES', 'MX', 'AR', 'CL', 'CO', 'PE'],
        'it': ['IT'],
        'pt': ['PT', 'BR'],
        'nl': ['NL', 'BE'],
        'ru': ['RU'],
        'zh': ['CN', 'TW', 'HK'],
        'ja': ['JP'],
        'ko': ['KR'],
        'ar': ['AE', 'SA', 'EG'],
        'tr': ['TR'],
        'pl': ['PL'],
        'sv': ['SE'],
        'no': ['NO'],
        'fi': ['FI'],
        'da': ['DK'],
        'cs': ['CZ'],
        'hu': ['HU'],
        'ro': ['RO'],
        'el': ['GR'],
        'th': ['TH'],
        'vi': ['VN'],
        'id': ['ID'],
        'he': ['IL'],
    }
    
    # Timezones mapped to regions
    timezones = {
        'US': ['America/New_York', 'America/Los_Angeles', 'America/Chicago', 'America/Denver', 'America/Phoenix'],
        'GB': ['Europe/London'],
        'CA': ['America/Toronto', 'America/Vancouver', 'America/Montreal'],
        'AU': ['Australia/Sydney', 'Australia/Melbourne', 'Australia/Brisbane', 'Australia/Perth'],
        'NZ': ['Pacific/Auckland'],
        'IE': ['Europe/Dublin'],
        'ZA': ['Africa/Johannesburg'],
        'IN': ['Asia/Kolkata', 'Asia/Mumbai'],
        'SG': ['Asia/Singapore'],
        'MY': ['Asia/Kuala_Lumpur'],
        'PH': ['Asia/Manila'],
        'DE': ['Europe/Berlin', 'Europe/Munich'],
        'AT': ['Europe/Vienna'],
        'CH': ['Europe/Zurich'],
        'FR': ['Europe/Paris'],
        'BE': ['Europe/Brussels'],
        'ES': ['Europe/Madrid'],
        'MX': ['America/Mexico_City'],
        'AR': ['America/Buenos_Aires'],
        'CL': ['America/Santiago'],
        'CO': ['America/Bogota'],
        'PE': ['America/Lima'],
        'IT': ['Europe/Rome'],
        'PT': ['Europe/Lisbon'],
        'BR': ['America/Sao_Paulo', 'America/Rio_Branco'],
        'NL': ['Europe/Amsterdam'],
        'RU': ['Europe/Moscow', 'Asia/Vladivostok'],
        'CN': ['Asia/Shanghai', 'Asia/Beijing'],
        'TW': ['Asia/Taipei'],
        'HK': ['Asia/Hong_Kong'],
        'JP': ['Asia/Tokyo'],
        'KR': ['Asia/Seoul'],
        'AE': ['Asia/Dubai'],
        'SA': ['Asia/Riyadh'],
        'EG': ['Africa/Cairo'],
        'TR': ['Europe/Istanbul'],
        'PL': ['Europe/Warsaw'],
        'SE': ['Europe/Stockholm'],
        'NO': ['Europe/Oslo'],
        'FI': ['Europe/Helsinki'],
        'DK': ['Europe/Copenhagen'],
        'CZ': ['Europe/Prague'],
        'HU': ['Europe/Budapest'],
        'RO': ['Europe/Bucharest'],
        'GR': ['Europe/Athens'],
        'TH': ['Asia/Bangkok'],
        'VN': ['Asia/Ho_Chi_Minh'],
        'ID': ['Asia/Jakarta'],
        'IL': ['Asia/Jerusalem'],
    }
    
    # Select random language
    lang = random.choice(languages)
    
    # Select random region for that language
    region = random.choice(regions[lang])
    
    # Build locale
    locale = f"{lang}-{region}"
    
    # Get appropriate timezone
    timezone = random.choice(timezones.get(region, ['UTC']))
    
    return {
        'locale': locale,
        'timezone': timezone,
        'country': region,
        'language': lang,
    }


def get_ultra_random_fingerprint() -> Dict:
    """
    Generate an ultra-random browser fingerprint using randomized generators.
    This creates completely unique combinations never seen before.
    """
    # Generate random components
    user_agent = generate_random_user_agent()
    locale_tz = generate_random_locale_timezone()
    
    # Random viewport from pool
    viewport = random.choice(VIEWPORTS)
    
    return {
        'user_agent': user_agent,
        'viewport': viewport,
        'locale': locale_tz['locale'],
        'timezone_id': locale_tz['timezone'],
        'country': locale_tz['country'],
        'language': locale_tz['language'],
        'device_scale_factor': random.choice(DEVICE_SCALE_FACTORS),
        'color_scheme': random.choice(COLOR_SCHEMES),
        'has_touch': random.choice(HAS_TOUCH_OPTIONS),
        'hardware_concurrency': random.choice(HARDWARE_CONCURRENCY),
        'device_memory': random.choice(DEVICE_MEMORY),
    }


def get_batch_random_fingerprints(count: int) -> List[Dict]:
    """
    Generate multiple unique fingerprints at once.
    Ensures maximum diversity across a batch.
    
    Args:
        count: Number of unique fingerprints to generate
    
    Returns:
        List of fingerprint dictionaries
    """
    fingerprints = []
    used_combinations = set()
    
    max_attempts = count * 10  # Prevent infinite loop
    attempts = 0
    
    while len(fingerprints) < count and attempts < max_attempts:
        fingerprint = get_ultra_random_fingerprint()
        
        # Create a unique signature for this fingerprint
        signature = (
            fingerprint['user_agent'][:50],  # First 50 chars
            fingerprint['locale'],
            fingerprint['timezone_id'],
        )
        
        # Only add if unique
        if signature not in used_combinations:
            used_combinations.add(signature)
            fingerprints.append(fingerprint)
        
        attempts += 1
    
    return fingerprints
