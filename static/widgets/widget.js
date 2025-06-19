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
        width: 55px;
        height: 55px;
        background-color: #ebbecb;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        z-index: 9999;
        font-size: 20px;
      }

      #bestseller-popup {
        position: fixed;
        bottom: 90px;
        left: 20px;
        width: 300px;
        background: white;
        border-radius: 12px;
        padding: 10px;
        border: 3px solid #ebbecb; /* 🔴 Daha kalın pembe çerçeve */
        box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        overflow-y: auto;
        max-height: 70vh;
        z-index: 9999;
        display: none;
      }

      #bestseller-popup h2 {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 8px;
      }

      .bestseller-product-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 6px;
      }

      .bestseller-product-wrapper {
        width: 47%;
        border: 1px solid #ebbecb;
        padding: 6px;
        border-radius: 6px;
        background: #fff;
        box-sizing: border-box;
      }

      .bestseller-product-img {
        position: relative;
      }

      .bestseller-base-image,
      .bestseller-hover-image {
        width: 100%;
        border-radius: 4px;
        display: block;
      }

      .bestseller-hover-image {
        position: absolute;
        top: 0;
        left: 0;
        opacity: 0;
        transition: opacity 0.3s ease;
      }

      .bestseller-product-img:hover .bestseller-hover-image {
        opacity: 1;
      }

      .bestseller-product-detail {
        text-align: center;
        margin-top: 6px;
      }

      .bestseller-product-title {
        display: block;
        color: #000;
        font-size: 12px;
        line-height: 1.2;
        margin-bottom: 2px;
        text-decoration: none;
      }

      .bestseller-price-wrapper {
        font-size: 13px;
        font-weight: bold;
        color: #000;
      }

      .bestseller-discover-button {
        margin-top: 4px;
        display: inline-block;
        font-size: 11px;
        padding: 4px 10px;
        background-color: #ebbecb;
        color: #000;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 500;
      }

      @media (max-width: 480px) {
        #bestseller-popup {
          left: 10px;
          width: 92vw;
          max-width: 300px;
        }

        .bestseller-product-wrapper {
          width: 47%;
        }

        .bestseller-product-title {
          font-size: 11px;
        }

        .bestseller-price-wrapper {
          font-size: 12px;
        }
      }
    `;

    const css = document.createElement("style");
    css.innerText = style;

    const toggle = document.createElement("div");
    toggle.id = "bestseller-toggle";
    toggle.innerText = "🛍️";
    toggle.onclick = () => {
      const popup = document.getElementById("bestseller-popup");
      state.visible = !state.visible;
      popup.style.display = state.visible ? "block" : "none";
    };

    const popup = document.createElement("div");
    popup.id = "bestseller-popup";
    popup.innerHTML = `
      <h2>ÇOK SATANLAR</h2>
      <div class="bestseller-product-grid">
        ${state.products
          .map(
            (p) => `
          <div class="bestseller-product-wrapper">
            <div class="bestseller-product-img">
              <a href="${p.url}">
                <img class="bestseller-base-image" src="${p.image_url}" alt="${p.name}" />
                <img class="bestseller-hover-image" src="${p.hover_image_url || p.image_url}" alt="${p.name}" />
              </a>
            </div>
            <div class="bestseller-product-detail">
              <a href="${p.url}" class="bestseller-product-title">${p.name}</a>
              <p class="bestseller-price-wrapper">${parseFloat(p.price).toLocaleString("tr-TR")} TL</p>
              <a href="${p.url}" class="bestseller-discover-button">Keşfet</a>
            </div>
          </div>`
          )
          .join("")}
      </div>
    `;

    container.appendChild(css);
    container.appendChild(toggle);
    container.appendChild(popup);
    document.body.appendChild(container);
  }

  window.addEventListener("load", fetchProducts);
})();
