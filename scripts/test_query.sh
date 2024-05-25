

kli init --name single1 --salt 0ABL1IHVUTvbzgbYUZ8MfMPI --nopasscode 

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
