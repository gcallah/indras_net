import React, { Component } from "react";
import { Loader, Dimmer } from "semantic-ui-react";
import axios from "axios";
import { Link } from "react-router-dom";
import Carousel from "./Carousel.js";
import sandpile_img from "./images/Sandpile.jpg";
import sandpile1_img from "./images/sandpile_2.png";
import mandelobrot_img from "./images/mendelobrot_sq.jpg";
class Home extends Component {
  api_server = "https://indrasnet.pythonanywhere.com/";
  state = {
    msg: "",
    allItems: [],
    loadingData: false,
    dataForCarousel: [
      { image: sandpile_img, title: "by Seth Terashima" },
      { image: sandpile1_img, title: "by Colt Browninga" },
      { image: mandelobrot_img, title: "by Adam majewski" }
    ]
  };

  async componentDidMount() {
    try {
      this.setState({ loadingData: true });
      document.title = "Indra | Home";
      const res = await axios.get(this.api_server + "models");
      this.setState({ allItems: res.data });
      this.setState({ loadingData: false });
      const doc = localStorage.getItem("doc");
      this.setState({ doc: doc });
      console.log("data-->", this.state.allItems);
    } catch (e) {
      console.log(e.message);
    }
  }

  openDescription = () => {
    const link = "https://gcallah.github.io/indras_net/index.html";
    window.open(link);
  };

  renderShowDescription = () => {
    console.log("renderShowDescription called");
    return (
      <h1 style={{ fontSize: 16, fontWeight: "400" }}>
        <a href="#" className="text-primary m-2" onClick={this.openDescription}>
          View Project Description{" "}
        </a>{" "}
      </h1>
    );
  };

  handleClick(id, name, source) {
    console.log(localStorage);
    localStorage.setItem("menu_id", id);
    localStorage.setItem("name", name);
    localStorage.setItem("source", source);
  }

  renderHeader = () => {
    return <h1 className="text-center">Indra Agent-Based Modeling System</h1>;
  };

  renderChooseModelProp = () => {
    return (
      <h1 style={{ fontSize: 16, fontWeight: "400" }}>
        Please choose a model:{" "}
      </h1>
    );
  };

  render() {
    if (this.state.loadingData) {
      return (
        <Dimmer active inverted>
          <Loader size="massive">Loading...</Loader>
        </Dimmer>
      );
    }
    const data = this.state.dataForCarousel;
    return (
      <div className="container">
        <div style={{ marginBottom: 100 }}>{this.renderHeader()}</div>
        <div className="row">
          <div className="col-6">
            {this.renderChooseModelProp()}
            <ul className="list-group">
              <div className="row">
                <div className="col">
                  {Object.keys(this.state.allItems).map((item, i) => (
                    <li
                      className="w-75 p-3 list-group-item list-group-item-action"
                      key={i}
                    >
                      {console.log(this.state.allItems)}
                      <Link
                        to={{
                          pathname: `/models/props/${
                            this.state.allItems[item]["model ID"]
                          }`
                        }}
                        className="text-primary"
                        data-toggle="tooltip"
                        data-placement="top"
                        title={this.state.allItems[item]["doc"]}
                        onClick={() =>
                          this.handleClick(
                            this.state.allItems[item]["model ID"],
                            this.state.allItems[item]["name"],
                            this.state.allItems[item]["source"]
                          )
                        }
                      >
                        {this.state.allItems[item]["name"]}
                      </Link>
                    </li>
                  ))}
                </div>
              </div>
            </ul>
            {this.renderShowDescription()}
          </div>
          <div className="col-6">
            <Carousel
              speed={5000}
              autoplay={true}
              className="col-12"
              data={data}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
