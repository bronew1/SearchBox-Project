(function () {
  console.log("👀 Benzer ürün widget başlatıldı...");

  function startWidget(productId) {
    if (!productId) {
      console.error("❌ product_id alınamadı, widget iptal edildi.");
      return;
    }

    console.log("🟢 Widget başlatılıyor, product_id:", productId);

    fetch(`https://searchprojectdemo.com/api/also-viewed-products/${productId}/`)
      .then(res => res.json())
      .then(data => {
        if (!data || data.length === 0) {
          console.log("🟡 Benzer ürün bulunamadı.");
          return;
        }

        const container = document.createElement("div");
        container.style.position = "fixed";
        container.style.bottom = "20px";
        container.style.left = "20px";
        container.style.zIndex = "9999";
        container.style.background = "#fff";
        container.style.border = "1px solid #ccc";
        container.style.padding = "10px";
        container.style.boxShadow = "0 0 10px rgba(0,0,0,0.2)";
        container.innerHTML = "<h4>Benzer Ürünler</h4>";

        data.forEach(item => {
          const el = document.createElement("div");
          el.innerHTML = `
            <a href="/product/${item.id}" target="_blank" style="display:block;margin-bottom:8px;">
              <img src="${item.image_url}" alt="${item.name}" style="width:80px;height:auto;">
              <div>${item.name} - ${item.price} TL</div>
            </a>
          `;
          container.appendChild(el);
        });

        document.body.appendChild(container);
      })
      .catch(err => {
        console.error("❌ Widget API hatası:", err);
      });
  }

  function listenForProductIdFromEvents() {
    const originalPush = window.dataLayer?.push;

    if (!originalPush) {
      console.error("❌ dataLayer bulunamadı.");
      return;
    }

    window.dataLayer.push = function () {
      const args = Array.from(arguments);
      args.forEach((arg) => {
        if (arg.event === "view_item" && arg.product_id) {
          console.log("📦 product_id bulundu:", arg.product_id);
          startWidget(arg.product_id);
        }
      });
      return originalPush.apply(this, arguments);
    };

    // Eğer dataLayer zaten doluysa geçmiş eventleri tara
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.forEach(event => {
        if (event.event === "view_item" && event.product_id) {
          console.log("📦 Önceki eventten product_id:", event.product_id);
          startWidget(event.product_id);
        }
      });
    }
  }

  listenForProductIdFromEvents();
})();
