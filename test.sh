#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0

check_status() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  local body="$4"

  if [ "$actual" -eq "$expected" ]; then
    echo -e "  ${GREEN}✅ PASS${NC} — $label (HTTP $actual)"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}❌ FAIL${NC} — $label (expected $expected, got $actual)"
    FAIL=$((FAIL + 1))
  fi
  echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
  echo ""
}

# ════════════════════════════════════════════════
echo -e "${CYAN}╔══════════════════════════════════╗${NC}"
echo -e "${CYAN}║         AUTH TESTS               ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════╝${NC}\n"

# ── 1. Signup ────────────────────────────────────
echo -e "${YELLOW}[1] POST /signup — new user${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/signup" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "pass1234"}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Signup new user" 200 "$STATUS" "$BODY"
TOKEN=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null)

# ── 2. Signup duplicate ──────────────────────────
echo -e "${YELLOW}[2] POST /signup — duplicate email${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/signup" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "pass1234"}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Signup duplicate email" 400 "$STATUS" "$BODY"

# ── 3. Login valid ───────────────────────────────
echo -e "${YELLOW}[3] POST /login — valid credentials${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "pass1234"}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Login valid" 200 "$STATUS" "$BODY"
TOKEN=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null)
echo -e "  ${GREEN}→ Token captured: ${TOKEN:0:40}...${NC}\n"

# ── 4. Login wrong password ──────────────────────
echo -e "${YELLOW}[4] POST /login — wrong password${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "wrongpass"}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Login wrong password" 401 "$STATUS" "$BODY"

# ── 5. Login unknown user ────────────────────────
echo -e "${YELLOW}[5] POST /login — unknown user${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "ghost@example.com", "password": "pass1234"}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Login unknown user" 401 "$STATUS" "$BODY"


# ════════════════════════════════════════════════
echo -e "${CYAN}╔══════════════════════════════════╗${NC}"
echo -e "${CYAN}║         PROFILE TESTS            ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════╝${NC}\n"

# ── 6. Get profile (none yet) ────────────────────
echo -e "${YELLOW}[6] GET /profile — no profile yet${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/profile" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get profile (empty)" 200 "$STATUS" "$BODY"

# ── 7. Create profile ────────────────────────────
echo -e "${YELLOW}[7] POST /profile — create profile${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Test User",
    "creator_type": "individual",
    "organization_type": null,
    "experience_level": "beginner",
    "audience_type": "general",
    "platform": "instagram",
    "goals": "Grow my audience and post consistently",
    "niches": ["tech", "lifestyle"]
  }')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Create profile" 200 "$STATUS" "$BODY"

# ── 8. Get profile (after create) ───────────────
echo -e "${YELLOW}[8] GET /profile — after creation${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/profile" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get profile (populated)" 200 "$STATUS" "$BODY"

# ── 9. Update profile (upsert) ───────────────────
echo -e "${YELLOW}[9] POST /profile — update existing profile${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "Updated User",
    "creator_type": "startup",
    "organization_type": "brand",
    "experience_level": "intermediate",
    "audience_type": "professionals",
    "platform": "linkedin",
    "goals": "Build a professional brand",
    "niches": ["business", "marketing"]
  }')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Update profile (upsert)" 200 "$STATUS" "$BODY"

# ── 10. Profile without token ────────────────────
echo -e "${YELLOW}[10] GET /profile — no token (expect 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/profile")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get profile unauthorized" 401 "$STATUS" "$BODY"

# ── 11. Create profile without token ─────────────
echo -e "${YELLOW}[11] POST /profile — no token (expect 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/profile" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "Hacker", "niches": []}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Create profile unauthorized" 401 "$STATUS" "$BODY"


# ════════════════════════════════════════════════
echo -e "${CYAN}╔══════════════════════════════════╗${NC}"
echo -e "${CYAN}║         DRAFTS TESTS             ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════╝${NC}\n"

# ── 12. List drafts (empty) ──────────────────────
echo -e "${YELLOW}[12] GET /drafts — empty list${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "List drafts (empty)" 200 "$STATUS" "$BODY"

# ── 13. Create draft ─────────────────────────────
echo -e "${YELLOW}[13] POST /drafts — create draft${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/drafts/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "hook": "Did you know 90% of creators quit in year one?",
      "script": "Here is why consistency beats talent every time...",
      "hashtags": ["#creator", "#consistency", "#growth"],
      "references": ["https://example.com/study"]
    }
  }')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Create draft" 200 "$STATUS" "$BODY"
DRAFT_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
echo -e "  ${GREEN}→ Draft ID captured: $DRAFT_ID${NC}\n"

# ── 14. List drafts (after create) ───────────────
echo -e "${YELLOW}[14] GET /drafts — after create${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "List drafts (populated)" 200 "$STATUS" "$BODY"

# ── 15. Get single draft ─────────────────────────
echo -e "${YELLOW}[15] GET /drafts/:id — get by id${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/$DRAFT_ID" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get draft by ID" 200 "$STATUS" "$BODY"

# ── 16. Update draft ─────────────────────────────
echo -e "${YELLOW}[16] PUT /drafts/:id — update draft${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/drafts/$DRAFT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "hook": "Updated hook: The secret to viral content is...",
      "script": "Updated script content here",
      "hashtags": ["#viral", "#content"],
      "references": []
    }
  }')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Update draft" 200 "$STATUS" "$BODY"

# ── 17. Get non-existent draft ───────────────────
echo -e "${YELLOW}[17] GET /drafts/99999 — not found${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/99999" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get draft not found" 404 "$STATUS" "$BODY"

# ── 18. Delete non-existent draft ────────────────
echo -e "${YELLOW}[18] DELETE /drafts/99999 — not found${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/drafts/99999" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Delete draft not found" 404 "$STATUS" "$BODY"

# ── 19. Delete draft ─────────────────────────────
echo -e "${YELLOW}[19] DELETE /drafts/:id — delete draft${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/drafts/$DRAFT_ID" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Delete draft" 200 "$STATUS" "$BODY"

# ── 20. Get draft after delete ───────────────────
echo -e "${YELLOW}[20] GET /drafts/:id — after delete (expect 404)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/$DRAFT_ID" \
  -H "Authorization: Bearer $TOKEN")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Get draft after delete" 404 "$STATUS" "$BODY"

# ── 21. Drafts without token ─────────────────────
echo -e "${YELLOW}[21] GET /drafts — no token (expect 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/drafts/")
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "List drafts unauthorized" 401 "$STATUS" "$BODY"

# ── 22. Create draft without token ───────────────
echo -e "${YELLOW}[22] POST /drafts — no token (expect 401)${NC}"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/drafts/" \
  -H "Content-Type: application/json" \
  -d '{"content": {"hook": "test"}}')
BODY=$(echo "$RESPONSE" | head -n -1)
STATUS=$(echo "$RESPONSE" | tail -n1)
check_status "Create draft unauthorized" 401 "$STATUS" "$BODY"


# ════════════════════════════════════════════════
TOTAL=$((PASS + FAIL))
echo -e "${CYAN}╔══════════════════════════════════╗${NC}"
echo -e "${CYAN}║           SUMMARY                ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════╝${NC}"
echo -e "  ${GREEN}✅ Passed: $PASS / $TOTAL${NC}"
if [ "$FAIL" -gt 0 ]; then
  echo -e "  ${RED}❌ Failed: $FAIL / $TOTAL${NC}"
else
  echo -e "  ${GREEN}🎉 All tests passed!${NC}"
fi
echo ""