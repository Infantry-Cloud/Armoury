{{/* Name of every control-plane object: <release>-control-plane. */}}
{{- define "control-plane.fullname" -}}
{{- printf "%s-control-plane" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "control-plane.selectorLabels" -}}
app.kubernetes.io/name: armoury-control-plane
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "control-plane.labels" -}}
{{ include "control-plane.selectorLabels" . }}
app.kubernetes.io/part-of: armoury
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end -}}

{{/* The image by digest; rendering fails without one, so nothing floats. */}}
{{- define "control-plane.image" -}}
{{- $ref := required "control-plane.image.ref is required (repository@sha256:<digest>)" .Values.image.ref -}}
{{- if not (contains "@sha256:" $ref) -}}
{{- fail (printf "control-plane.image.ref must be pinned by digest, got %q" $ref) -}}
{{- end -}}
{{- $ref -}}
{{- end -}}
