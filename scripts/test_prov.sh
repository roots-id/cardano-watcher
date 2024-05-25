kli init --name single1 --salt 0ABL1IHVUTvbzgbYUZ8MfMPI --nopasscode 

kli oobi resolve --name single1 --oobi http://witness1.dev.provenant.net:5631/oobi/BCf29L_7oQtU8WUXEV2Bi5sf7WoxnGyX7sgJSym-p4Pp/controller --oobi-alias dev01
kli oobi resolve --name single1 --oobi http://witness2.dev.provenant.net:5631/oobi/BFNdkltTbYsSxu3lDsKF4jWmUS54WD_Pdqxrts3_wzlF/controller --oobi-alias dev02

kli incept --name single1 --alias aid2 -w BCf29L_7oQtU8WUXEV2Bi5sf7WoxnGyX7sgJSym-p4Pp -w BFNdkltTbYsSxu3lDsKF4jWmUS54WD_Pdqxrts3_wzlF  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint




kli init --name single1 --salt 0ABL1IHVUTvbzgbYUZ8MfMPI --nopasscode 

kli oobi resolve --name single1 --oobi http://witness4.stage.provenant.net:5631/oobi/BO_zDhNmQs-zd6yjMRiKPZjQbo78bpa9Kt9bo2e2YFUL/controller --oobi-alias dev01
kli oobi resolve --name single1 --oobi http://witness5.stage.provenant.net:5631/oobi/BNFbib-oPD6bmFCN8LnCJADWVv8QLQCATeNKbkerF-lm/controller --oobi-alias dev02

kli incept --name single1 --alias aid2 -w BO_zDhNmQs-zd6yjMRiKPZjQbo78bpa9Kt9bo2e2YFUL -w BNFbib-oPD6bmFCN8LnCJADWVv8QLQCATeNKbkerF-lm  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint




kli init --name single1 --salt 0ABL1IHVUTvbzgbYUZ8MfMPI --nopasscode 

kli oobi resolve --name single1 --oobi http://localhost:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller --oobi-alias dev01
kli oobi resolve --name single1 --oobi http://localhost:5643/oobi/BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM/controller --oobi-alias dev02

kli incept --name single1 --alias aid2 -w BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha -w BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint
