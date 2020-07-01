import React, { createElement } from "react";
import ReactDOM from "react-dom";
import MessageField from "./components/MessageField";
// import "./styles/styles.css";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

const mountPoint = document.getElementById("root");
ReactDOM.render(
  <MuiThemeProvider>
    <MessageField />
  </MuiThemeProvider>,
  mountPoint
);
