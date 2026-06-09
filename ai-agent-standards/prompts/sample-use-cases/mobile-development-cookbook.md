---
id: PROMPT-007
version: 1.0
author: AI Agent Coding Framework
last_updated: 2026-05-13
applicable_stack: [Kotlin, Swift, Dart/Flutter, React Native, Jetpack Compose, SwiftUI]
category: Mobile_Development
difficulty: Intermediate
domain: General
---

# Prompt: Mobile Development — Safe AI-Assisted Code Generation

**Purpose:** Standardized prompt template for AI agents generating mobile application code. Covers Android, iOS, and cross-platform development with mobile-specific safety constraints that AI commonly violates.

---

## [CONTEXT]

- **Platform:** [Android / iOS / Cross-platform]
- **Tech stack:** [Kotlin + Jetpack Compose / Swift + SwiftUI / Dart + Flutter / React Native]
- **Architecture:** [MVVM / MVI / Clean Architecture]
- **Current state:** [Brief description of existing module structure]
- **Target API level:** [Android API 26+ / iOS 16+ / etc.]

### Mobile-Specific Context (provide to AI)
```
- Minimum SDK / deployment target: [version]
- Existing dependency injection: [Hilt / Koin / Swinject / none]
- State management: [ViewModel / StateFlow / Riverpod / Redux]
- Network layer: [Retrofit / Ktor / Alamofire / Dio]
- Local storage: [Room / CoreData / Hive / SQLite]
- CI/CD: [Fastlane / GitHub Actions / Bitrise]
```

---

## [TASK]

**Objective:** [Describe the mobile feature to build]

**Acceptance Criteria:**
- [ ] Feature works offline (if applicable)
- [ ] Handles configuration changes (rotation, split-screen) without data loss
- [ ] Respects platform lifecycle (no leaks on destroy/background)
- [ ] Permissions requested at runtime with rationale (not at install)
- [ ] Loading, error, and empty states all implemented
- [ ] Accessible: content descriptions, minimum touch targets (48dp/44pt)
- [ ] Unit tests for business logic (>= 80% coverage)

---

## [CONSTRAINTS]

### Karpathy Principles Enforcement

**Principle 1 — Think Before Coding:**
- State assumptions about minimum SDK, screen sizes, and permissions
- If the task involves a platform API that changed recently, note API level differences

**Principle 2 — Simplicity First:**
- No premature abstractions — one screen does not need a full Clean Architecture setup
- Use platform-standard components (Material 3 / Cupertino) — no custom UI when system components work
- If a feature can use a platform API, don't add a library

**Principle 3 — Surgical Changes:**
- Add new files only — do not restructure existing packages/folders
- Match existing naming convention (camelCase / snake_case per platform)
- Do not migrate existing code to new patterns unless requested

**Principle 4 — Goal-Driven Execution:**
- Define success as: "Feature works on [platform], handles lifecycle correctly, tests pass"
- Test on both portrait and landscape (or state why not applicable)

### FORBIDDEN — Common AI Mistakes on Mobile
- ❌ **No hardcoded dimensions** — use `dp`/`sp` (Android), dynamic units (iOS), not `px`
- ❌ **No blocking the main thread** — network/DB calls must be async (coroutines / async-await / Dispatchers.IO)
- ❌ **No context leaks** — never store Activity/Context in static fields or singletons
- ❌ **No ignored lifecycle** — cancel coroutines/subscriptions in `onDestroy`/`onDisappear`/`dispose`
- ❌ **No install-time permissions** — request at runtime with rationale dialog
- ❌ **No hardcoded strings** — use string resources for localization readiness
- ❌ **No unhandled deep links** — validate all incoming intent/URL data
- ❌ **No secrets in client code** — API keys in BuildConfig/Secrets or server-side proxy
- ❌ **No unrestricted network trust** — enforce certificate pinning for sensitive endpoints
- ❌ **No raw SQL on mobile** — use ORM/type-safe queries (Room / CoreData / Drift)

### REQUIRED
- ✅ Structured error handling with user-facing messages (not stack traces)
- ✅ Loading state for all async operations (skeleton / shimmer / indicator)
- ✅ Empty state UI when list/data is empty
- ✅ Offline fallback: cache-first strategy or clear "no connection" message
- ✅ Memory-conscious: no full-size bitmaps in memory, use image loading libraries
- ✅ Battery-conscious: no unnecessary background work, use WorkManager/BGTaskScheduler
- ✅ Proguard/R8 rules (Android) or equivalent obfuscation considered
- ✅ Accessibility: contentDescription / accessibilityLabel on interactive elements

### Process
- ✅ Run Self-Check before output
- ✅ Include Self-Check report

---

## [OUTPUT FORMAT]

- **Format:** Platform-specific source files:
  - UI layer (Compose / SwiftUI / Widget / Component)
  - ViewModel / Bloc / Controller
  - Repository / Data source
  - Unit tests
- **Style:** Platform conventions (Kotlin style guide / Swift API guidelines / Dart effective style)
- **Include:** Self-Check report

### Expected Code Structure

**Android (Kotlin + Compose):**
```
feature/
├── ui/
│   └── FeatureScreen.kt          # Composable UI
├── viewmodel/
│   └── FeatureViewModel.kt       # State + logic
├── data/
│   ├── FeatureRepository.kt      # Data access
│   └── local/FeatureDao.kt       # Room DAO (if needed)
└── model/
    └── FeatureUiState.kt         # Sealed class for states
```

**iOS (Swift + SwiftUI):**
```
Feature/
├── Views/
│   └── FeatureView.swift          # SwiftUI view
├── ViewModels/
│   └── FeatureViewModel.swift     # ObservableObject
├── Services/
│   └── FeatureService.swift       # Data access
└── Models/
    └── FeatureModel.swift         # Data models
```

**Cross-platform (Flutter / React Native):**
```
feature/
├── screens/
│   └── feature_screen.[dart/tsx]  # UI
├── providers/ or hooks/
│   └── feature_provider.[dart/ts] # State management
├── services/
│   └── feature_service.[dart/ts]  # Data access
└── models/
    └── feature_model.[dart/ts]    # Data models
```

### Expected Self-Check (Mobile-Specific)
```markdown
## Self-Check Report (Mobile)
- [ ] No main thread blocking (async for network/DB)
- [ ] Lifecycle handled (cancellation on destroy)
- [ ] No context/activity leaks
- [ ] No hardcoded strings (string resources used)
- [ ] No secrets in client code
- [ ] Loading / error / empty states present
- [ ] Accessibility labels on interactive elements
- [ ] Works offline or shows clear offline message
- [ ] Unit tests pass (>= 80% coverage on logic)
```

---

## Reference

- Prompt Template Standard: [`../PROMPT-TEMPLATE.md`](../PROMPT-TEMPLATE.md)
- Security Constraints: [`../../risk-management/security-constraints.md`](../../risk-management/security-constraints.md)
- Hallucination Detection: [`../../quality-control/hallucination-detection.md`](../../quality-control/hallucination-detection.md)
- Android Guidelines: https://developer.android.com/develop/ui/compose/state
- iOS Guidelines: https://developer.apple.com/design/human-interface-guidelines
- Flutter Best Practices: https://docs.flutter.dev/perf/best-practices
