/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Slider from 'react-slick';
import propTypes from 'prop-types';

class Carousel extends Component {
  renderImage = () => {
    const {
      dots, speed, autoplay, className, data,
    } = this.props;
    const settings = {
      dots,
      infinite: true,
      speed,
      slidesToShow: 1,
      slidesToScroll: 1,
      autoplay,
      fade: true,
      className,
    };
    return (
      <div>
        <Slider {...settings}/* eslint-disable-line react/jsx-props-no-spreading */>
          {data.map((item) => (
            <div key={item.title}>
              <img
                src={item.image}
                className="rounded-circle carousel"
                alt="Responsive Model"
                data-toggle="tooltip"
                data-placement="top"
                title={item.title}
              />
            </div>
          ))}
        </Slider>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderImage()}
      </div>
    );
  }
}

Carousel.propTypes = {
  dots: propTypes.bool,
  speed: propTypes.number,
  autoplay: propTypes.bool,
  data: propTypes.arrayOf,
};

Carousel.defaultProps = {
  dots: false,
  speed: 1000,
  autoplay: false,
  data: [],
};

export default Carousel;
