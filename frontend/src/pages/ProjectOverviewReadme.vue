<template>
  <!-- Updated by Omar Jaber -->
  <ReadmeEditor
    :resource="project"
    fieldname="readme"
    :border="true"
    :collapsible="true"
    :editable="!project.doc.archived_at && this.$user().role=='Gameplan Admin'"
  />
</template>
<script>
import ReadmeEditor from '@/components/ReadmeEditor.vue'
export default {
  name: 'ProjectOverviewReadme',
  props: ['project'],
  components: { ReadmeEditor },
}
</script>
