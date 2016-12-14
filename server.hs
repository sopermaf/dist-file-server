import Network
import Control.Concurrent
import System.IO
 
main = withSocketsDo $ do
    sock <- listenOn $ PortNumber 5002
    loop sock
 
loop sock = do
   (h,_,_) <- accept sock
   forkIO $ body h
   loop sock
  where
   body h = do
       s <- readFile "server.hs"
       hPutStr h s
       hFlush h
       hClose h
       
msg = "hello world"
