import { createContext,useState } from "react";

export const GlobalContext=createContext(null)

const GlobalState=({children})=>{
    const [on, setOn] = useState("")


    return(
        <GlobalContext.Provider value={{on,setOn}}>

            {children}
        </GlobalContext.Provider>
    )
}

export default GlobalState