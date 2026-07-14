<template>
  <section>
    <h1>Places</h1>

    <div class="place-list" v-if="places.length">
      <article
        v-for="place in places"
        :key="place.contentId"
        class="place-card"
      >
        <button type="button" class="place-button" @click="openPlace(place)">
          <img :src="place.thumbnailUrl" alt="" class="place-thumbnail" />
          <div class="place-info">
            <h2>{{ place.title }}</h2>
            <p>{{ place.contentType }} · {{ place.region }}</p>
            <p>{{ place.address }}</p>
            <p class="tags">{{ place.tags.join(' · ') }}</p>
          </div>
        </button>
      </article>
    </div>

    <div v-else>
      <p>No places to show.</p>
    </div>

    <PlaceDetailModal
      :show="showPlaceModal"
      :place="selectedPlace"
      @update:show="showPlaceModal = $event"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mockPlaces from '../data/mockPlaces'
import PlaceDetailModal from '../components/PlaceDetailModal.vue'

const places = ref([])
const selectedPlace = ref(null)
const showPlaceModal = ref(false)

function openPlace(place) {
  selectedPlace.value = place
  showPlaceModal.value = true
}

onMounted(async () => {
  places.value = mockPlaces
})
</script>

<style>
.place-list {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  margin-top: 24px;
}
.place-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}
.place-button {
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
}
.place-thumbnail {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.place-info {
  padding: 16px;
}
.place-info h2 {
  margin: 0 0 8px;
  font-size: 1.1rem;
}
.tags {
  margin-top: 12px;
  color: #666;
  font-size: 0.95rem;
}
</style>