import React, { Component } from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import propTypes from 'prop-types';

class Carousel extends Component {

    constructor(props) {
        super(props)
    }

    renderImage = () => {
        let settings = {
              dots: this.props.dots,
              infinite: true,
              speed: this.props.speed,
              slidesToShow: 1,
              slidesToScroll: 1,
              autoplay: this.props.autoplay,
              fade:true,
              className: this.props.className,
            };
        return <div>
            <Slider {...settings}>
                 {this.props.data.map((item,index) => {
                     return <div key ={index}>
                        <img src={item['image']}
                        className="rounded-circle carousel"
                        alt="Responsive image"
                        data-toggle="tooltip" data-placement="top" title={item['title']}/>
                    </div>
                })}
            </Slider>
        </div>
    }

    render() {
        return (
             <div >
                 {this.renderImage()}
             </div>
        );
    }
}

Carousel.propTypes ={
    dots: propTypes.bool,
    speed: propTypes.number,
    autoplay: propTypes.bool,
    data: propTypes.array,
}

Carousel.defaultProps={
    dots: false,
    speed:1000,
    autoplay: false
}

export default Carousel;
