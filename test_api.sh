#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"

echo -e "${YELLOW}=== Secure LLM Inference Service - API Tests ===${NC}\n"

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
curl -X GET "$API_URL/health" | jq .
echo -e "\n"

# Test 2: Get Authentication Token
echo -e "${YELLOW}Test 2: Get Authentication Token${NC}"
TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo1234")

echo $TOKEN_RESPONSE | jq .
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')
echo -e "\n"

if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
  echo -e "${RED}Failed to get access token. Exiting.${NC}"
  exit 1
fi

# Test 3: Inference Request
echo -e "${YELLOW}Test 3: Inference Request${NC}"
curl -X POST "$API_URL/v1/infer" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about fast inference."}' | jq .
echo -e "\n"

# Test 4: Get Metrics
echo -e "${YELLOW}Test 4: Get Metrics${NC}"
curl -X GET "$API_URL/metrics" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
echo -e "\n"

# Test 5: Rate Limiting Test (send 12 requests)
echo -e "${YELLOW}Test 5: Rate Limiting (sending 12 requests rapidly)${NC}"
for i in {1..12}; do
  echo -e "Request $i:"
  curl -s -X POST "$API_URL/v1/infer" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello"}' | jq -r '.response // .detail'
  echo ""
done

echo -e "${GREEN}=== Tests Complete ===${NC}"