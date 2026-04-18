const REGISTRY_PATH = "./galleries/index.json";
const EMPTY_IMAGE = "./img/empty-state.svg";

export class GallerySystem {
  constructor() {
    this.state = {
      galleries: [],
      selectedTag: null,
      search: "",
      activeGallery: null,
      activePhotoIndex: 0,
    };

    this.elements = {
      gallerySearch: document.querySelector("#gallery-search"),
      clearFilters: document.querySelector("#clear-filters"),
      tagFilters: document.querySelector("#tag-filters"),
      galleryList: document.querySelector("#gallery-list"),
      galleryCount: document.querySelector("#gallery-count"),
      galleryView: document.querySelector("#gallery-view"),
      galleryTitle: document.querySelector("#gallery-title"),
      galleryDescription: document.querySelector("#gallery-description"),
      galleryImageCount: document.querySelector("#gallery-image-count"),
      galleryTags: document.querySelector("#gallery-tags"),
      photoGrid: document.querySelector("#photo-grid"),
      backToGalleries: document.querySelector("#back-to-galleries"),
      lightbox: document.querySelector("#lightbox"),
      lightboxImage: document.querySelector("#lightbox-image"),
      lightboxTitle: document.querySelector("#lightbox-title"),
      lightboxCaption: document.querySelector("#lightbox-caption"),
      lightboxPrev: document.querySelector("#lightbox-prev"),
      lightboxNext: document.querySelector("#lightbox-next"),
    };
  }

  async init() {
    this.bindEvents();
    await this.loadGalleries();
    this.renderFilters();
    this.renderGalleryCards();
    this.restoreFromHash();
  }

  bindEvents() {
    this.elements.gallerySearch.addEventListener("input", (event) => {
      this.state.search = event.target.value.trim().toLowerCase();
      this.renderGalleryCards();
    });

    this.elements.clearFilters.addEventListener("click", () => {
      this.state.selectedTag = null;
      this.state.search = "";
      this.elements.gallerySearch.value = "";
      this.renderFilters();
      this.renderGalleryCards();
    });

    this.elements.backToGalleries.addEventListener("click", () => {
      this.closeGalleryView();
    });

    this.elements.lightboxPrev.addEventListener("click", () => {
      this.stepLightbox(-1);
    });

    this.elements.lightboxNext.addEventListener("click", () => {
      this.stepLightbox(1);
    });

    window.addEventListener("hashchange", () => {
      this.restoreFromHash();
    });

    document.addEventListener("keydown", (event) => {
      if (!this.elements.lightbox.open) {
        return;
      }

      if (event.key === "ArrowLeft") {
        this.stepLightbox(-1);
      }

      if (event.key === "ArrowRight") {
        this.stepLightbox(1);
      }

      if (event.key === "Escape") {
        this.elements.lightbox.close();
      }
    });
  }

  async loadGalleries() {
    try {
      const response = await fetch(REGISTRY_PATH);
      if (!response.ok) {
        throw new Error(`Failed to load registry: ${response.status}`);
      }
      const registry = await response.json();
      const galleryRequests = registry.galleries.map((gallery) => this.loadGalleryManifest(gallery));
      this.state.galleries = await Promise.all(galleryRequests);
    } catch (error) {
      this.renderEmptyState(
        this.elements.galleryList,
        "Could not load the gallery registry.",
        "Check that /galleries/index.json exists and is valid JSON."
      );
      console.error(error);
    }
  }

  async loadGalleryManifest(gallery) {
    const response = await fetch(gallery.manifest);
    if (!response.ok) {
      throw new Error(`Failed to load gallery manifest: ${gallery.manifest}`);
    }
    const manifest = await response.json();
    return {
      ...manifest,
      id: gallery.id,
      manifest: gallery.manifest,
    };
  }

  getAllTags() {
    const tags = new Set();
    this.state.galleries.forEach((gallery) => {
      gallery.tags.forEach((tag) => tags.add(tag));
    });
    return [...tags].sort((a, b) => a.localeCompare(b));
  }

  getFilteredGalleries() {
    return this.state.galleries.filter((gallery) => {
      const matchesTag = !this.state.selectedTag || gallery.tags.includes(this.state.selectedTag);
      const haystack = [gallery.title, gallery.description, ...(gallery.tags || [])]
        .join(" ")
        .toLowerCase();
      const matchesSearch = !this.state.search || haystack.includes(this.state.search);
      return matchesTag && matchesSearch;
    });
  }

  renderFilters() {
    const tags = this.getAllTags();
    if (!tags.length) {
      this.elements.tagFilters.innerHTML = "";
      return;
    }

    this.elements.tagFilters.innerHTML = tags
      .map((tag) => {
        const activeClass = this.state.selectedTag === tag ? " is-active" : "";
        return `<button class="tag${activeClass}" type="button" data-tag="${tag}">${tag}</button>`;
      })
      .join("");

    this.elements.tagFilters.querySelectorAll("[data-tag]").forEach((button) => {
      button.addEventListener("click", () => {
        this.state.selectedTag = this.state.selectedTag === button.dataset.tag ? null : button.dataset.tag;
        this.renderFilters();
        this.renderGalleryCards();
      });
    });
  }

  renderGalleryCards() {
    const galleries = this.getFilteredGalleries();
    this.elements.galleryCount.textContent = `${galleries.length} ${galleries.length === 1 ? "gallery" : "galleries"} visible`;

    if (!galleries.length) {
      this.renderEmptyState(
        this.elements.galleryList,
        "No galleries match the current search.",
        "Try clearing filters or adjust the search phrase."
      );
      return;
    }

    this.elements.galleryList.innerHTML = galleries
      .map(
        (gallery) => `
          <article class="gallery-card">
            <div class="gallery-card__media">
              <img src="${gallery.cover}" alt="${gallery.title} cover image">
            </div>
            <div class="gallery-card__body">
              <h3>${gallery.title}</h3>
              <p>${gallery.description}</p>
              <div class="tag-list tag-list--compact">
                ${gallery.tags.map((tag) => `<span class="tag">${tag}</span>`).join("")}
              </div>
              <button class="gallery-card__button" type="button" data-open-gallery="${gallery.id}">
                Open gallery
              </button>
            </div>
          </article>
        `
      )
      .join("");

    this.elements.galleryList.querySelectorAll("[data-open-gallery]").forEach((button) => {
      button.addEventListener("click", () => {
        this.openGallery(button.dataset.openGallery);
      });
    });
  }

  openGallery(galleryId) {
    const gallery = this.state.galleries.find((entry) => entry.id === galleryId);
    if (!gallery) {
      return;
    }

    this.state.activeGallery = gallery;
    this.elements.galleryView.hidden = false;
    this.elements.galleryTitle.textContent = gallery.title;
    this.elements.galleryDescription.textContent = gallery.description;
    this.elements.galleryImageCount.textContent = gallery.images.length;
    this.elements.galleryTags.innerHTML = gallery.tags.map((tag) => `<span class="tag">${tag}</span>`).join("");
    this.elements.photoGrid.innerHTML = gallery.images
      .map(
        (image, index) => `
          <article class="photo-card">
            <div class="photo-card__media">
              <img src="${image.src}" alt="${image.alt}">
            </div>
            <div class="photo-card__body">
              <h3>${image.title}</h3>
              <p>${image.caption}</p>
              <button class="gallery-card__button" type="button" data-open-photo="${index}">
                View image
              </button>
            </div>
          </article>
        `
      )
      .join("");

    this.elements.photoGrid.querySelectorAll("[data-open-photo]").forEach((button) => {
      button.addEventListener("click", () => {
        this.openLightbox(Number(button.dataset.openPhoto));
      });
    });

    window.location.hash = `gallery=${gallery.id}`;
    this.elements.galleryView.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  closeGalleryView() {
    this.state.activeGallery = null;
    this.elements.galleryView.hidden = true;
    this.elements.photoGrid.innerHTML = "";
    if (this.elements.lightbox.open) {
      this.elements.lightbox.close();
    }
    history.replaceState(null, "", window.location.pathname);
  }

  openLightbox(index) {
    if (!this.state.activeGallery) {
      return;
    }

    this.state.activePhotoIndex = index;
    const image = this.state.activeGallery.images[index];
    this.elements.lightboxImage.src = image.src;
    this.elements.lightboxImage.alt = image.alt;
    this.elements.lightboxTitle.textContent = image.title;
    this.elements.lightboxCaption.textContent = image.caption;

    if (!this.elements.lightbox.open) {
      this.elements.lightbox.showModal();
    }
  }

  stepLightbox(direction) {
    if (!this.state.activeGallery) {
      return;
    }

    const total = this.state.activeGallery.images.length;
    const nextIndex = (this.state.activePhotoIndex + direction + total) % total;
    this.openLightbox(nextIndex);
  }

  restoreFromHash() {
    const hash = window.location.hash.replace(/^#/, "");
    if (!hash.startsWith("gallery=")) {
      return;
    }

    const galleryId = hash.replace("gallery=", "");
    const gallery = this.state.galleries.find((entry) => entry.id === galleryId);
    if (gallery) {
      this.openGallery(galleryId);
    }
  }

  renderEmptyState(container, title, message) {
    container.innerHTML = `
      <div class="empty-state">
        <img src="${EMPTY_IMAGE}" alt="">
        <div>
          <h3>${title}</h3>
          <p>${message}</p>
        </div>
      </div>
    `;
  }
}
