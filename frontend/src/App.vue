<script>
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";

export default {
  data() {
    return {};
  },
  components: {
    Navbar,
    Footer,
  },
};
</script>

<template>
  <Navbar />
  <router-view />
  <Footer />
</template>

<style scoped></style>
