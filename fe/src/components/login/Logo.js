import React from 'react'
import knight from '../../knight.jpg'
import '../App.css'

const Logo = props => (
  <div className="logo-container">
    <h1 className="logo-text">Chess</h1>
    <img className="logo-img" src={knight}/>
  </div>
)


export default Logo