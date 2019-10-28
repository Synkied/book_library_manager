<template>
	<v-layout row wrap>
		<v-dialog
			:value=true
			persistent
			@keydown.esc="$emit('close')"
			:overlay="false"
			max-width="500px"
			@close="contentDeleteConfirmation = false"
			transition="dialog-transition">
			<v-card>
				<v-toolbar dense>
		      <v-toolbar-title class="overline">{{ toolbarMsg }}</v-toolbar-title>
		      <v-btn icon>
		        <v-icon>close</v-icon>
		      </v-btn>
				</v-toolbar>
				<v-card-text class="pt-3">
					{{ bodyMsg }}
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn depressed :ref="cancelBtnText" @click="$emit('close')">
						{{ cancelBtnText }}
					</v-btn>
					<v-btn depressed :ref="okBtnText" color="primary" class="background--text" @click="$emit('action', data); $emit('close')">
						{{ okBtnText }}
					</v-btn>
					</v-card-actions>
			</v-card>
		</v-dialog>
	</v-layout>
</template>

<script>

export default {
	props: ['toolbarMsg', 'bodyMsg', 'okBtnText', 'cancelBtnText', 'autofocus'],
	data () {
		return {
			data: ''
		}
	},
	mounted () {
		if (this.autofocus) {
			this.$refs[this.autofocus].$el.focus()
		}
	}
}
</script>
