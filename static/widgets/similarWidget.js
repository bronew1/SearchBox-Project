(function () {
  var interval = setInterval(function () {
    if (!window.dataLayer || !window.dataLayer.length) return;

    // dataLayer içinde product_id içeren objeyi bul
    var productEvent = window.dataLayer.find(function (event) {
      return event.event === "view_item" && event.product_id;
    });

    if (!productEvent) return;

    var sku = productEvent.product_id;
    if (!sku) return;

    clearInterval(interval); // Ürün kodu bulunduysa kontrolü durdur

    var apiUrl = "https://searchprojectdemo.com/api/recommendations/similar/" + sku + "/";

    var xhr = new XMLHttpRequest();
    xhr.open("GET", apiUrl, true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        try {
          var data = JSON.parse(xhr.responseText);
          var products = data.products || [];

          if (products.length === 0) return;

          // CSS
          var style = document.createElement("style");
          style.innerHTML = `
            #similar-products-slider {
              padding: 20px;
              margin-top: 40px;
              border-top: 1px solid #ccc;
              font-family: sans-serif;
            }
            #similar-products-slider h2 {
              font-size: 20px;
              margin-bottom: 12px;
            }
            .similar-products-grid {
              display: flex;
              overflow-x: auto;
              gap: 12px;
            }
            .similar-product-card {
              flex: 0 0 200px;
              border: 1px solid #eee;
              border-radius: 8px;
              padding: 10px;
              background: #fff;
              text-align: center;
            }
            .similar-product-card img {
              max-width: 100%;
              height: auto;
            }
            .similar-product-card .price {
              font-weight: bold;
              margin-top: 4px;
            }
          `;
          document.head.appendChild(style);

          // HTML
          var container = document.createElement("div");
          container.id = "similar-products-slider";
          container.innerHTML = "<h2>Benzer Ürünler</h2>";

          var grid = document.createElement("div");
          grid.className = "similar-products-grid";

          for (var j = 0; j < products.length; j++) {
            var p = products[j];
            var card = document.createElement("div");
            card.className = "similar-product-card";

            card.innerHTML =
              '<a href="' +
              p.url +
              '"><img src="' +
              p.image +
              '" alt="' +
              p.name +
              '" /><div>' +
              p.name +
              '</div><div class="price">' +
              p.price +
              ' TL</div></a>';

            grid.appendChild(card);
          }

          container.appendChild(grid);

          // Konum: .product-detail elementinden sonra ekle
          var target = document.querySelector(".product-detail");
          if (target) {
            target.insertAdjacentElement("afterend", container);
          } else {
            document.body.appendChild(container); // fallback
          }

        } catch (e) {
          console.error("Benzer ürünler parse edilemedi:", e);
        }
      }
    };
    xhr.send();
  }, 300); // Her 300ms'de bir dataLayer kontrolü
})();
