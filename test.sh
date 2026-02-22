#!/usr/bin/env bash

BASE_URL="https://trendbackend.onrender.com"

echo "LOGIN"
TOKEN=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"pass1234\"}" | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
echo "TOKEN=$TOKEN"
echo ""

echo "GET PROFILE"
curl -X GET "$BASE_URL/profile" -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

echo "CREATE PROFILE"
curl -X POST "$BASE_URL/profile" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"display_name\":\"Test\",\"creator_type\":\"individual\",\"experience_level\":\"beginner\",\"audience_type\":\"general\",\"platform\":\"instagram\",\"goals\":\"Grow\",\"niches\":[\"tech\"]}"
echo ""
echo ""

echo "LIST DRAFTS"
curl -X GET "$BASE_URL/drafts/" -H "Authorization: Bearer $TOKEN"
echo ""
echo ""

echo "CREATE DRAFT"
curl -X POST "$BASE_URL/drafts/" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"content\":{\"hook\":\"hello\",\"script\":\"world\"}}"
echo ""
echo ""

echo "DONE