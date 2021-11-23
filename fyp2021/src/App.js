import React, { useState } from "react";
import "./App.css";

import { BrowserRouter, Route, Switch, NavLink } from "react-router-dom";
import Home from "./home.js";
import identified from "./identify.js";

function App() {
	return (
		<div className="App">
			<BrowserRouter>
				<div className="Background">
					<div className="Header">
						<div className="H1">MHW2102</div>
						<div className="H2">Fruit Recognizer</div>
					</div>
					<div className="bar"> </div>
					<NavLink to="/" exact></NavLink>
					<NavLink to="/identified"></NavLink>
					<Switch>
						<Route component={Home} path="/" exact />
						<Route component={identified} path="/identified" exact />
					</Switch>
				</div>
			</BrowserRouter>
		</div>
	);
}

export default App;
