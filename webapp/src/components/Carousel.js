import React, { Component } from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";


class Carousel extends Component {
    renderImage = () => {
        const sandpile_img = require('./images/Sandpile.jpg')
        var settings = {
              dots: true,
              infinite: true,
              speed: 500,
              slidesToShow: 1,
              slidesToScroll: 1,
              autoplay: true
            };
        //Please add the path of the images we wish to use in the carousel to the ListOfImages list.
        var ListOfImages = [sandpile_img,sandpile_img,sandpile_img]
        return <div>
            <Slider {...settings}>
                 {ListOfImages.map((pathOfImage,index) => {
                     return <div key ={index}>
                        <img src={pathOfImage}
                        className="rounded-circle"
                        alt="Responsive image"
                        style={{display:'block', width:'100%', alignItems: "center"}}
                        data-toggle="tooltip" data-placement="top" title="by Seth Terashima."/>
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

export default Carousel;
