import React from "react";
import img from'../../assets/IMAGE 2025-03-15 21:44:59.jpg';

const Logo = () => (
  <div className="flex items-center gap-2">
    <div className="relative w-20 h-20">
          <img src={img} alt="Skywire" />
    </div>
  </div>
);

export default Logo;