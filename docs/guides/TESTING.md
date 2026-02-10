# Spec 008: Testing Documentation

## Overview

This document outlines the testing strategy for Spec 008 Chat Interface implementation, covering both backend unit/integration tests and frontend component tests.

## Backend Testing

### Test Suites

| Test Suite | Location | Tests | Coverage |
|------------|----------|-------|----------|
| Conversation Continuation | `tests/test_conversation_continuation.py` | 23 | Full conversation flow with 10+ messages |
| History Service | `tests/test_history_service.py` | 13 | History reconstruction and validation |
| Chat Endpoint | `tests/test_chat_endpoint.py` | 12+ | Stateless chat API endpoints |
| **TOTAL** | - | **48** | **100% of core functionality** |

### Running Backend Tests

```bash
cd backend
pytest tests/test_conversation_continuation.py -v
pytest tests/test_history_service.py -v
pytest tests/test_chat_endpoint.py -v
```

### Backend Test Coverage

#### Conversation Continuation (T037-T047)
- ✅ Conversation ID validation (T037)
- ✅ Parameter handling with optional conversation_id (T038)
- ✅ Load existing conversation (T039)
- ✅ Update timestamp on activity (T040)
- ✅ Reconstruct history in chronological order (T041-T042)
- ✅ Test with 10+ messages (T043)
- ✅ Mixed user/assistant roles (T044)
- ✅ Context integrity validation (T045)

#### History Service (T046-T047)
- ✅ get_conversation_history() method
- ✅ verify_message_ordering() validation
- ✅ format_for_agent() formatting
- ✅ validate_context_integrity() checks
- ✅ get_conversation_summary() generation
- ✅ reconstruct_with_validation() full flow

#### Chat Endpoint (T021-T036)
- ✅ POST /api/{user_id}/chat endpoint
- ✅ GET /api/{user_id}/conversations list
- ✅ GET /api/{user_id}/conversations/{id}/history
- ✅ JWT authentication (T024)
- ✅ Conversation creation (T026)
- ✅ User message persistence BEFORE agent (T027)
- ✅ Agent orchestration with 30s timeout (T028-T032)
- ✅ Response persistence AFTER agent (T034)
- ✅ Error handling for all HTTP status codes

---

## Frontend Testing

### Test Suites (T059)

| Component | Test File | Test Cases | Status |
|-----------|-----------|-----------|--------|
| ChatInterface | `ChatInterface.test.tsx` | 20+ | ✅ COMPLETE |
| MessageList | `MessageList.test.tsx` | 25+ | ✅ COMPLETE |
| Message | `Message.test.tsx` | 15+ | ✅ COMPLETE |
| MessageInput | `MessageInput.test.tsx` | 25+ | ✅ COMPLETE |
| LoadingIndicator | `LoadingIndicator.test.tsx` | 12+ | ✅ COMPLETE |
| ErrorDisplay | `ErrorDisplay.test.tsx` | 30+ | ✅ COMPLETE |
| ToolCallDisplay | `ToolCallDisplay.test.tsx` | 30+ | ✅ COMPLETE |
| **TOTAL** | - | **157+** | ✅ **COMPLETE** |

### Running Frontend Tests

```bash
cd frontend
npm test -- --testMatch="**/*.test.tsx"
npm test -- ChatInterface.test.tsx
npm test -- Message.test.tsx
npm test -- MessageInput.test.tsx
npm test -- MessageList.test.tsx
npm test -- LoadingIndicator.test.tsx
npm test -- ErrorDisplay.test.tsx
npm test -- ToolCallDisplay.test.tsx
```

### Frontend Test Coverage

#### ChatInterface Component (T048)
- ✅ Initial render with header and empty state
- ✅ Message input field rendering and updates
- ✅ Send button enable/disable based on input
- ✅ Error handling (NO_AUTH, UNAUTHORIZED, FETCH_ERROR)
- ✅ Error dismissal functionality
- ✅ Loading indicator display and input disable
- ✅ Message display and chronological ordering
- ✅ Conversation creation and history loading
- ✅ JWT token retrieval from localStorage
- ✅ API integration with POST /api/{user_id}/chat

#### MessageList Component (T049)
- ✅ Renders all messages in order
- ✅ Handles empty message list
- ✅ Single and multiple message rendering
- ✅ Chronological ordering (oldest to newest)
- ✅ Large message list handling (100+ messages)
- ✅ Tool call integration
- ✅ Mixed user/assistant messages
- ✅ Special characters and long content handling

#### Message Component (T053-T056)
- ✅ User message styling (blue, right-aligned, "You" label)
- ✅ Assistant message styling (gray, left-aligned, "Assistant" label)
- ✅ Timestamp display in HH:mm format
- ✅ Tool call rendering when present
- ✅ Whitespace preservation in content
- ✅ Long message handling
- ✅ Different styling for different roles

#### MessageInput Component (T050-T052)
- ✅ Text input field rendering
- ✅ Send button rendering and state
- ✅ onChange callback on user input
- ✅ Form submission on send button click
- ✅ Ctrl+Enter submission support
- ✅ Disabled state during loading
- ✅ Empty state disable logic
- ✅ Multiline input support
- ✅ JWT token header inclusion

#### LoadingIndicator Component (T057)
- ✅ Loading indicator rendering
- ✅ Animated spinner display
- ✅ "Agent is thinking..." message
- ✅ Blue color scheme
- ✅ Proper animation classes

#### ErrorDisplay Component (T058)
- ✅ Error message display
- ✅ Error code display
- ✅ Error icon rendering
- ✅ Dismissible with close button
- ✅ Error code to title mapping:
  - NO_AUTH → "Authentication Required"
  - UNAUTHORIZED → "Session Expired"
  - FORBIDDEN → "Access Denied"
  - NOT_FOUND → "Not Found"
  - AGENT_TIMEOUT → "Agent Timeout"
  - SEND_ERROR → "Failed to Send Message"
  - FETCH_ERROR → "Failed to Load Conversation"
- ✅ Red color scheme
- ✅ onDismiss callback

#### ToolCallDisplay Component (T055)
- ✅ Tool name header rendering
- ✅ Expand/collapse functionality
- ✅ Parameters display as formatted JSON
- ✅ Result display as formatted JSON
- ✅ Execution timestamp display
- ✅ Expand/collapse indicator (▶/▼)
- ✅ Complex nested object handling
- ✅ Multiple tool calls support
- ✅ Proper styling with gray background

---

## Visual Regression Testing (T060)

### Screenshot Comparison Strategy

Visual regression testing compares rendered component screenshots to catch unintended visual changes. This can be implemented using:

#### Approach 1: Storybook + Chromatic (Recommended)

```bash
# Install Storybook
npx storybook@latest init

# Create stories for each component
# frontend/src/components/ChatInterface.stories.tsx
# frontend/src/components/Message.stories.tsx
# frontend/src/components/MessageInput.stories.tsx
# etc.

# Run locally
npm run storybook

# Connect to Chromatic for automatic visual regression
npx chromatic --project-token=<token>
```

#### Approach 2: Percy.io Integration

```bash
# Install Percy CLI
npm install --save-dev @percy/cli @percy/react

# Add Percy script to package.json
"percy": "percy exec -- npm test"

# Run with Percy
npm run percy
```

#### Approach 3: Playwright Visual Comparisons

```typescript
// frontend/e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test('ChatInterface visual regression', async ({ page }) => {
  await page.goto('/chat/user-123');
  await expect(page).toHaveScreenshot('chat-interface.png');
});

test('Message styling regression', async ({ page }) => {
  await page.goto('/chat/user-123');
  const message = page.locator('[role="article"]').first();
  await expect(message).toHaveScreenshot('user-message.png');
});

test('Error display regression', async ({ page }) => {
  // Simulate error state
  await page.evaluate(() => {
    window.simulateError?.('NO_AUTH', 'Authentication required');
  });
  await expect(page).toHaveScreenshot('error-display.png');
});
```

### Manual Visual Testing Checklist

When running visual regression tests manually, verify:

#### Component Layout (T048-T058)
- [ ] ChatInterface renders full-screen with header, messages, input
- [ ] Header displays "Chat Assistant" title and conversation ID/new chat status
- [ ] Message list fills available space with proper scrolling
- [ ] Input area fixed at bottom with form layout
- [ ] All components have proper spacing (padding/margin)

#### Message Styling (T053-T054)
- [ ] User messages appear blue on right side
- [ ] Assistant messages appear gray on left side
- [ ] "You" and "Assistant" labels display correctly
- [ ] Message text wraps properly without overflow
- [ ] Timestamps align with message content

#### Tool Call Display (T055)
- [ ] Tool names show as collapsible headers
- [ ] Parameters display as readable JSON when expanded
- [ ] Results display as readable JSON when expanded
- [ ] Expand/collapse arrows show correct direction
- [ ] Pre-formatted text blocks have proper styling

#### Loading State (T057)
- [ ] Loading indicator shows spinner animation
- [ ] "Agent is thinking..." message displays
- [ ] Spinner rotates continuously
- [ ] Input field becomes disabled during loading
- [ ] Loading indicator center-aligned

#### Error Display (T058)
- [ ] Error message displays in red box
- [ ] Error code shows in small gray text
- [ ] Error title matches code (e.g., NO_AUTH → "Authentication Required")
- [ ] Close button visible and functional
- [ ] Error appears above input field

#### Input Field (T050-T052)
- [ ] Textarea accepts multi-line text
- [ ] Send button shows "Send" text normally
- [ ] Send button shows "Sending..." when disabled
- [ ] Button aligns properly with textarea
- [ ] Placeholder text displays when empty

#### Responsive Design
- [ ] ChatInterface works on mobile (< 640px)
- [ ] ChatInterface works on tablet (640px - 1024px)
- [ ] ChatInterface works on desktop (> 1024px)
- [ ] Message list scrolls smoothly on all sizes
- [ ] Input field remains accessible on mobile

### Taking Baseline Screenshots

```bash
# First-time setup - create baseline images
npm test -- --updateSnapshot

# Or with Percy
npm run percy -- npm test

# Or with Playwright
npx playwright test --update-snapshots
```

### Comparing Against Baseline

```bash
# Run tests and compare to baseline
npm test -- ChatInterface.test.tsx

# With Percy - automatic comparison
npm run percy -- npm test

# With Playwright
npx playwright test --reporter=html
```

---

## Integration Testing

### End-to-End Flow Testing

Test the full conversation flow from UI to backend:

```bash
# Start backend
cd backend
python -m uvicorn src.main:app --reload

# Start frontend
cd frontend
npm run dev

# Run e2e tests (with Playwright, Cypress, or Playwright)
npx playwright test
```

### Manual E2E Test Scenario

1. **New Conversation**
   - [ ] User opens chat interface
   - [ ] "Start a new conversation" message displays
   - [ ] Type message in input field
   - [ ] Click Send or press Ctrl+Enter
   - [ ] Loading indicator appears
   - [ ] User message appears in blue
   - [ ] Agent response appears in gray
   - [ ] Conversation ID is generated

2. **Continue Conversation**
   - [ ] User navigates to existing conversation
   - [ ] Previous messages load and display in order
   - [ ] User adds new message
   - [ ] New message appends to list
   - [ ] Agent responds with context

3. **Error Handling**
   - [ ] No auth token → "Authentication Required" error
   - [ ] Session expires → "Session Expired" error
   - [ ] Network fails → "Failed to send message" error
   - [ ] Dismiss error → error disappears

4. **Tool Call Display**
   - [ ] Agent executes tool
   - [ ] Tool call appears under message as "Tools Used:"
   - [ ] Click tool name to expand
   - [ ] Parameters and result display as JSON
   - [ ] Timestamp shows when tool was executed

---

## Performance Testing

### Load Testing Checklist

- [ ] Render 100+ messages without lag
- [ ] Scroll smoothly through large message lists
- [ ] Input remains responsive during loading
- [ ] No memory leaks with repeated send/clear
- [ ] WebSocket or API response under 5 seconds

### Browser DevTools Testing

```javascript
// Measure paint timing
performance.getEntriesByType('paint').forEach(entry => {
  console.log(`${entry.name}: ${entry.startTime}ms`);
});

// Measure Largest Contentful Paint (LCP)
new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    console.log('LCP:', entry.renderTime || entry.loadTime);
  });
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

---

## Summary

### Test Coverage
- **Backend**: 48 tests covering all core API and database functionality
- **Frontend**: 157+ tests covering all UI components and user interactions
- **Visual**: Manual testing checklist and screenshot comparison approach
- **E2E**: Manual scenario testing for full conversation flows
- **Performance**: Load testing checklist and browser metrics

### Test Execution
- Backend tests run with `pytest` (deterministic, unit-focused)
- Frontend tests run with Jest/React Testing Library (user-behavior focused)
- Visual tests via Storybook + Chromatic, Percy, or Playwright
- E2E tests manually or with Playwright/Cypress

### Next Steps
1. Set up CI/CD to run all tests on every commit
2. Implement visual regression with Chromatic or Percy
3. Add load testing with k6 or Apache JMeter
4. Monitor test coverage trends in each phase
