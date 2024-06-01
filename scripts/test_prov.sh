echo; read -rsn1 -p "Press any key to continue ..."; echo


printf "%s " "result 1"

echo; read -rsn1 -p "Press any key to continue . . ."; echo

printf "%s " "Result 2"



curl -X POST --data '{"alias":"aid2","prefix":"EBedz7uSzReTQcb0P54QmA82EeGoH1-wwOjx9xU8sCVS","watched":true,"cardano":false,"oobi":"http://127.0.0.1:5642/oobi/EBedz7uSzReTQcb0P54QmA82EeGoH1-wwOjx9xU8sCVS/witness/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha"}' --header "Content-Type: application/json" localhost:8000/aids
