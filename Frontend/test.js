import React, { Component } from 'react';

export default class test extends Component {
	render() {
		return (
			<div class="container" style="margin-top:60px;">
				<div class="dashboard">
					<div class="dashboard-map">
						<div class="map">
							{/* <!-- <input id="address-input" placeholder="Type an address" type="text"> --> */}
							<div class="ui icon fluid input">
								<input id="address-input2" type="text" placeholder="Search..." />
								<i aria-hidden="true" class="search icon" />
							</div>
							<div id="map" />
							<script src="./index.js" />
							<script
								src="https://maps.googleapis.com/maps/api/js?key='YOUR_KEY'&callback=initMap&sensor=false&libraries=places"
								async
								defer
							/>
							<div id="city-name">Pick your HouseHover over your city</div>
						</div>
					</div>
					<div class="dashboard-info">{/* <div id="city-name"> </div> */}</div>
				</div>
			</div>
		);
	}
}
