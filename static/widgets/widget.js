(function () {
  const state = { visible: false, products: [] };

  function fetchProducts() {
    fetch("https://searchprojectdemo.com/api/product/widget-products/")
      .then((res) => res.json())
      .then((data) => {
        state.products = data.products;
        renderPopup();
      });
  }

  function renderPopup() {
    const container = document.createElement("div");
    container.id = "bestseller-widget";

    const style = `
      #bestseller-toggle {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 65px;
        height: 65px;
        background-color: #ebbecb;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        z-index: 9999;
        font-size: 24px;
      }

      #bestseller-popup {
        position: fixed;
        bottom: 100px;
        left: 20px;
        width: 92vw;
        max-width: 520px;
        height: auto;
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #ebbecb;
        box-shadow: 0 2px 20px rgba(0,0,0,0.2);
        overflow-y: auto;
        z-index: 9999;
        display: none;
      }

      #bestseller-popup h2 {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 12px;
      }

      .bestseller-product-wrapper {
        width: 48%;
        float: left;
        box-sizing: border-box;
        margin: 1%;
        border: 1px solid #ebbecb;
        padding: 8px;
        border-radius: 6px;
        background: #fff;
      }

      .bestseller-product-img {
        position: relative;
      }

      .bestseller-base-image, .bestseller-hover-image {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 6px;
      }

      .bestseller-hover-image {
        position: absolute;
        top: 0;
        left: 0;
        opacity: 0;
        transition: opacity 0.3s;
      }

      .bestseller-product-img:hover .bestseller-hover-image {
        opacity: 1;
      }

      .bestseller-hover-img-detail {
        position: absolute;
        bottom: 10px;
        left: 10px;
        color: white;
        font-size: 12px;
      }

      .bestseller-product-code {
        background: rgba(0,0,0,0.6);
        padding: 2px 6px;
        border-radius: 4px;
      }

      .bestseller-product-detail {
        text-align: center;
        margin-top: 8px;
      }

      .bestseller-product-title {
        display: block;
        color: #000;
        font-size: 13px;
        text-decoration: none;
        margin-bottom: 4px;
      }

      .bestseller-price-wrapper {
        font-size: 14px;
        font-weight: bold;
        color: #000;
      }

      @media (max-width: 480px) {
        #bestseller-popup {
          width: 90vw;
          left: 5vw;
          bottom: 90px;
          padding: 12px;
        }

        .bestseller-product-wrapper {
          width: 48%;
          margin: 1%;
        }
      }
    `;

    const css = document.createElement("style");
    css.innerText = style;

    const toggle = document.createElement("div");
    toggle.id = "bestseller-toggle";
    toggle.innerText = "🛍️";
    toggle.onclick = () => {
      state.visible = !state.visible;
      document.getElementById("bestseller-popup").style.display = state.visible ? "block" : "none";
    };

    const popup = document.createElement("div");
    popup.id = "bestseller-popup";
    popup.innerHTML = `
      <h2>ÇOK SATANLAR</h2>
      ${state.products.map((p) => `
        <div class="bestseller-product-wrapper">
          <div class="bestseller-product-img">
            <a href="${p.url}">
              <img class="bestseller-base-image" src="${p.image_url}" alt="${p.name}" />
              <img class="bestseller-hover-image" src="${p.hover_image_url || p.image_url}" alt="${p.name}" />
            </a>
            <div class="bestseller-hover-img-detail">
              <div class="bestseller-product-code">${p.sku}</div>
            </div>
          </div>
          <div class="bestseller-product-detail">
            <a href="${p.url}" class="bestseller-product-title">${p.name}</a>
            <p class="bestseller-price-wrapper">${parseFloat(p.price).toLocaleString("tr-TR")} TL</p>
          </div>
        </div>
      `).join("")}
    `;

    container.appendChild(css);
    container.appendChild(toggle);
    container.appendChild(popup);
    document.body.appendChild(container);
  }

  window.addEventListener("load", fetchProducts);
})();
