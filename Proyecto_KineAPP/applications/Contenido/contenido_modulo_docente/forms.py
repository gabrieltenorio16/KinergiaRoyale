from django import forms
from applications.Contenido.models import Tema, Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import Paciente, CasoClinico, FichaClinicaEstudiante, Etapa

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ["titulo", "descripcion", "estado_completado", "fecha_inicio", "fecha_fin"]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Lesiones de rodilla en deportistas",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe brevemente el foco del tema…",
            }),
            "fecha_inicio": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "fecha_fin": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "estado_completado": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
        labels = {
            "titulo": "Título",
            "descripcion": "Descripción",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de finalización",
            "estado_completado": "Estado completado",
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["titulo", "url", "tema"]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Lesion de Menisco",
            }),
            "url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Pega aquí la URL del video",
            }),
            "tema": forms.Select(attrs={
                "class": "form-select",
            }),
        }
        labels = {
            "titulo": "Título",
            "url": "URL del video",
            "tema": "Tema asociado",
        }

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Trabajo",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Describe brevemente el tópico…",
            }),
        }
        labels = {
            "nombre": "Nombre del tópico",
            "descripcion": "Descripción",
        }


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ["pregunta", "topico"]
        widgets = {
            "pregunta": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe el enunciado de la pregunta…",
            }),
            "topico": forms.Select(attrs={
                "class": "form-select",
            }),
        }
        labels = {
            "pregunta": "Pregunta",
            "topico": "Tópico asociado",
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ["contenido", "retroalimentacion", "es_correcta", "pregunta"]
        widgets = {
            "contenido": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe el texto de la respuesta…",
            }),
            "retroalimentacion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Retroalimentación opcional para el estudiante…",
            }),
            "es_correcta": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "pregunta": forms.Select(attrs={
                "class": "form-select",
            }),
        }
        labels = {
            "contenido": "Contenido de la respuesta",
            "retroalimentacion": "Retroalimentación",
            "es_correcta": "¿Es la respuesta correcta?",
            "pregunta": "Pregunta asociada",
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["nombres", "apellidos", "edad", "antecedentes", "historial_medico"]
        widgets = {
            "nombres": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Felipe",
            }),
            "apellidos": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Durán",
            }),
            "edad": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
            "antecedentes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Antecedentes relevantes del paciente…",
            }),
            "historial_medico": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Resumen del historial médico…",
            }),
        }
        labels = {
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "edad": "Edad",
            "antecedentes": "Antecedentes",
            "historial_medico": "Historial médico",
        }

class CasoClinicoForm(forms.ModelForm):
    class Meta:
        model = CasoClinico
        fields = ["titulo", "descripcion", "paciente"]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Caso de esguince de tobillo",
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe brevemente el caso clínico…",
            }),
            "paciente": forms.Select(attrs={
                "class": "form-select",
            }),
        }
        labels = {
            "titulo": "Título del caso clínico",
            "descripcion": "Descripción",
            "paciente": "Paciente asociado",
        }

class FichaClinicaEstudianteForm(forms.ModelForm):
    class Meta:
        model = FichaClinicaEstudiante
        fields = [
            'nombre_paciente_ficha',
            'apellido_paciente_ficha',
            'edad_paciente_ficha',
            'anamnesis_actual',
            'motivo_consulta_ficha',
        ]
        widgets = {
            "nombre_paciente_ficha": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nombre(s) según la ficha del estudiante",
            }),
            "apellido_paciente_ficha": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Apellidos según la ficha del estudiante",
            }),
            "edad_paciente_ficha": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
            "anamnesis_actual": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
            }),
            "motivo_consulta_ficha": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
        }
        labels = {
            "nombre_paciente_ficha": "Nombres del Paciente",
            "apellido_paciente_ficha": "Apellidos del Paciente",
            "edad_paciente_ficha": "Edad del Paciente",
            "anamnesis_actual": "Anamnesis Actual",
            "motivo_consulta_ficha": "Motivo de Consulta",
        }

class EtapaForm(forms.ModelForm):
    class Meta:
        model = Etapa
        fields = ["nombre", "caso", "video"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Entrevista inicial – Rodilla derecha",
            }),
            "caso": forms.Select(attrs={
                "class": "form-select",
            }),
            "video": forms.Select(attrs={
                "class": "form-select",
            }),
        }
        labels = {
            "nombre": "Nombre de la entrevista",
            "caso": "Caso clínico",
            "video": "Video asociado",
        }
