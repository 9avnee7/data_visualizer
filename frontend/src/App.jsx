import { useState } from 'react'
import {createBrowserRouter , RouterProvider } from "react-router-dom";
import './App.css'
import Editor from './components/Editor/Editor';


const router=createBrowserRouter(
  [
      {
          path:'/',
          element:
          <div>

            <Editor/>

          </div>
          
      }
    ])
function App() {

  
  return (
    <>
     <RouterProvider router={router}/>
    </>
  )
}

export default App
