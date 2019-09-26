import React, { Component } from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import PropTypes from 'prop-types';

class Carousel extends Component {

    constructor(props) {
        super(props)
    }

    renderImage = () => {
        const sandpile_img = require('./images/Sandpile.jpg')
        const sandpile1_img = require('./images/sandpile_2.png')
        let settings = {
              dots: this.props.dots,
              infinite: true,
              speed: this.props.speed,
              slidesToShow: 1,
              slidesToScroll: 1,
              autoplay: this.props.autoplay
            };
        //Please add the path of the images we wish to use in the carousel to the ListOfImages list.
        let imageObj = [
            {   'image':sandpile_img,
                'title':"by Seth Terashima"},
            {   'image':sandpile1_img,
                'title':"by Colt Browninga"}
        ]


        return <div>
            <Slider {...settings}>
                 {imageObj.map((item,index) => {
                     return <div key ={index}>
                        <img src={item['image']}
                        className="rounded-circle"
                        alt="Responsive image"
                        style={{display:'block', width:'100%', alignItems: "center"}}
                        data-toggle="tooltip" data-placement="top" title={item['title']}/>
                    </div>
                })}
            </Slider>
        </div>
    }

    render() {
        return (
             <div className={this.props.className}>
                 {this.renderImage()}
             </div>
        );
    }
}

Carousel.PropTypes ={
    dots: PropTypes.bool,
    speed: PropTypes.number,
    autoplay: PropTypes.bool
}

Carousel.defaultProps={
    dots: true,
    speed:500,
    autoplay: false
}

export default Carousel;
