from typing import Dict

from pydantic import BaseModel, model_serializer, model_validator

from kenar.models.widgets.action import get_action, get_link_from_action
from kenar.models.widgets.base import BaseWidget


class WideButtonBar(BaseModel, BaseWidget):
    class Button(BaseModel):
        title: str
        link: str

        @model_serializer
        def ser_model(self) -> dict:
            return {'title': self.title} | get_action(link=self.link)

        @model_validator(mode='before')
        @classmethod
        def deserialize_button(cls, data: Dict) -> Dict:
            if 'action' in data:
                data['link'] = get_link_from_action(data.get('action', {}))
                data.pop('action', None)
            return data

    button: Button

    def serialize_model(self) -> dict:
        return {
            "widget_type": "WIDE_BUTTON_BAR",
            "data": {"@type": "type.googleapis.com/widgets.WideButtonBarWidgetData"} |
                    self.dict(exclude={'style'}) | {'style': 'SECONDARY'}
        }

    @classmethod
    def deserialize_model(cls, data: Dict):
        widget_data = data.get('data', {})
        widget_data.pop('@type', None)
        return cls.parse_obj(widget_data)
