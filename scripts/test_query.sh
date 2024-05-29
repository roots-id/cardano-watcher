

kli init --name single1  --nopasscode 

kli oobi resolve --name single1 --oobi https://witness-dev01.rootsid.cloud/oobi/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx/controller --oobi-alias dev01
kli oobi resolve --name single1 --oobi https://witness-dev02.rootsid.cloud/oobi/BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd/controller --oobi-alias dev02
kli oobi resolve --name single1 --oobi https://witness-dev03.rootsid.cloud/oobi/BNY3LWk2BzX8wXmkXuvpYRVSdfynanwKQwD80KOG00VH/controller --oobi-alias dev03

kli incept --name single1 --alias aid2 -w BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx -w BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint

kli status --name single1 --alias aid1


kli init --name watcher --salt 0ACrYPA-H0jBv9ux-_2xSSGI --nopasscode
kli oobi resolve --name watcher --oobi https://witness-dev01.rootsid.cloud/oobi/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx/controller --oobi-alias dev01
kli oobi resolve --name watcher --oobi https://witness-dev02.rootsid.cloud/oobi/BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd/controller --oobi-alias dev02
kli oobi resolve --name watcher --oobi https://witness-dev03.rootsid.cloud/oobi/BNY3LWk2BzX8wXmkXuvpYRVSdfynanwKQwD80KOG00VH/controller --oobi-alias dev03

kli oobi resolve --name watcher --oobi-alias aid1 --oobi https://witness-dev01.rootsid.cloud/oobi/EGCVIUpuoZlLi1QyMBbyM8ZQoDlqpyzQgj38NMyMJfvW/witness/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx

kli incept --name watcher --alias watcher  --toad 0 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable

kli query --name watcher --alias watcher --prefix EGCVIUpuoZlLi1QyMBbyM8ZQoDlqpyzQgj38NMyMJfvW 



kli incept --name single1 --alias aid4 -w BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx -w BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint


kli init --name watcher2 --salt 0ACrYPA-H0jBv9ux-_2xSSGI --nopasscode
kli oobi resolve --name watcher2 --oobi https://witness-dev01.rootsid.cloud/oobi/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx/controller --oobi-alias dev01
kli oobi resolve --name watcher2 --oobi https://witness-dev02.rootsid.cloud/oobi/BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd/controller --oobi-alias dev02
kli oobi resolve --name watcher2 --oobi https://witness-dev03.rootsid.cloud/oobi/BNY3LWk2BzX8wXmkXuvpYRVSdfynanwKQwD80KOG00VH/controller --oobi-alias dev03
kli oobi resolve --name watcher2 --oobi https://witness-dev01.rootsid.cloud/oobi/EI2myCV0wgWmgLcPewucZs-o_df2RBqlH7WV68qTCPo9/witness/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx --oobi-alias aid1



kli incept --name single1 --alias aid6 -w BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx -w BOUZ4v-vPMP5KyZQP-d_8B30UHI4KWgXczBgWcRJnnYd  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable --receipt-endpoint



kli oobi resolve --name watcher2 --oobi https://witness-dev01.rootsid.cloud/oobi/EI2myCV0wgWmgLcPewucZs-o_df2RBqlH7WV68qTCPo9/witness/BHI7yViNOGWd1X0aKMgxLm4dUgbQDYoCFSJM2U8Hb3cx --oobi-alias aid1




kli oobi resolve --name watcher2 --oobi http://127.0.0.1:5642/oobi/BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha/controller --oobi-alias dev01
kli oobi resolve --name watcher2 --oobi http://127.0.0.1:5643/oobi/BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM/controller --oobi-alias dev02




kli incept --name watcher2 --alias watcher3 -w BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha -w BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM  --toad 2 --icount 1 --isith 1 --ncount 1 --nsith 1 --transferable
