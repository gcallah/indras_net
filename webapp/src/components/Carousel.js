import React, { Component } from 'react';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import Slider from 'react-slick';
import PropTypes from 'prop-types';

class Carousel extends Component {
  constructor(props) {
    super(props);
    const imagesLoadedStatus = new Array(props.data.length).fill(false);
    this.state = {
      imagesLoadedStatus,
    };
  }

  renderImage = () => {
    const {
      dots, speed, autoplay, className, data,
    } = this.props;
    const settings = {
      arrows: false,
      dots,
      infinite: true,
      speed,
      slidesToShow: 1,
      slidesToScroll: 1,
      autoplay,
      fade: true,
      className,
    };
    const areAllImagesLoaded = () => {
      const { imagesLoadedStatus } = this.state;
      for (let i = 0; i < imagesLoadedStatus.length; i += 1) {
        if (!imagesLoadedStatus[i]) return false;
      }
      return true;
    };
    return (
      <div>
        <Slider
          {...settings} /* eslint-disable-line react/jsx-props-no-spreading */
        >
          {data.map((item, index) => (
            <div key={item.title}>
              {areAllImagesLoaded() ? null : <div>Loading...</div>}
              <img
                src={item.image}
                style={areAllImagesLoaded() ? {} : { display: 'none' }}
                className="rounded-circle carousel"
                alt="Responsive Model"
                data-toggle="tooltip"
                data-placement="top"
                title={item.title}
                onLoad={() => {
                  const { imagesLoadedStatus } = this.state;
                  const imagesLoadedStatusCopy = imagesLoadedStatus.slice();
                  imagesLoadedStatusCopy[index] = true;
                  this.setState({
                    imagesLoadedStatus: imagesLoadedStatusCopy,
                  });
                }}
              />
            </div>
          ))}
        </Slider>
      </div>
    );
  };

  render() {
    return (
      <div>
        {this.renderImage()}
      </div>
    );
  }
}

Carousel.propTypes = {
  dots: PropTypes.bool,
  speed: PropTypes.number,
  autoplay: PropTypes.bool,
  className: PropTypes.string,
  data: PropTypes.arrayOf(PropTypes.shape({
    image: PropTypes.string,
    title: PropTypes.string,
  })),
};

Carousel.defaultProps = {
  dots: false,
  speed: 1000,
  autoplay: false,
  className: '',
  data: [],
};

export default Carousel;
