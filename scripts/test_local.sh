# Resolve OOBI for demo witness
curl -X POST --data '{"alias":"wan","prefix":"BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha","provider":"local","oobi":"http://127.0.0.1:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller"}' --header "Content-Type: application/json" localhost:8000/witnesses
curl -X POST --data '{"alias":"wil","prefix":"BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM","provider":"local","oobi":"http://127.0.0.1:5643/oobi/BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM/controller"}' --header "Content-Type: application/json" localhost:8000/witnesses

kli init --name local1  --nopasscode --salt 0AAWO5C0o5sRN8z71RRcp0iQ

kli oobi resolve --name local1 --oobi http://127.0.0.1:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller --oobi-alias dev01
kli oobi resolve --name local1 --oobi http://127.0.0.1:5643/oobi/BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM/controller --oobi-alias dev02

kli incept --name local1 --alias aid1 -w BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha -w BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable
kli status --name local1 --alias aid1

curl -X POST --data '{"alias":"aid1","prefix":"EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9","watched":true,"cardano":false,"oobi":"http://127.0.0.1:5642/oobi/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9/witness/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha"}' --header "Content-Type: application/json" localhost:8000/aids


curl localhost:8000/aids/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9



kli rotate --name local1 --alias aid1

curl localhost:8000/aids/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9

kli rotate --name local1 --alias aid1

curl localhost:8000/aids/EF3V0uUvP3o4awSSNqJ9wUpG_BdamZgr9S9K_GLNWDZ9

