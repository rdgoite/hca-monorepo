package org.humancellatlas.ingest.messaging;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.FanoutExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.annotation.RabbitListenerConfigurer;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.core.RabbitMessagingTemplate;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.rabbit.listener.RabbitListenerEndpointRegistrar;
import org.springframework.amqp.rabbit.listener.SimpleMessageListenerContainer;
import org.springframework.amqp.rabbit.listener.adapter.MessageListenerAdapter;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.converter.MappingJackson2MessageConverter;
import org.springframework.messaging.converter.MessageConverter;
import org.springframework.messaging.handler.annotation.support.DefaultMessageHandlerMethodFactory;

/**
 * @author Simon Jupp
 * @date 04/09/2017 Samples, Phenotypes and Ontologies Team, EMBL-EBI
 */
@Configuration
public class QueueConfig implements RabbitListenerConfigurer {
    @Bean Queue queueFileUpdate() { return new Queue(Constants.Queues.FILE_UPDATE, false); }

    @Bean FanoutExchange fileExchange() { return new FanoutExchange(Constants.Exchanges.FILE_FANOUT); }

    @Bean Queue queueFileStaged() { return new Queue(Constants.Queues.FILE_STAGED, false); }

    @Bean FanoutExchange fileStagedExchange() { return new FanoutExchange(Constants.Exchanges.FILE_STAGED_FANOUT); }

    @Bean Queue queueEnvelopeSubmitted() { return new Queue(Constants.Queues.ENVELOPE_SUBMITTED, false); }

    @Bean FanoutExchange envelopeExchange() { return new FanoutExchange(Constants.Exchanges.ENVELOPE_FANOUT); }

    @Bean Queue queueValidationRequired() { return new Queue(Constants.Queues.VALIDATION_REQUIRED, false); }

    @Bean FanoutExchange validationExchange() { return new FanoutExchange(Constants.Exchanges.VALIDATION_FANOUT); }

    /* bindings */

    @Bean Binding bindingFileStaged(Queue queueFileStaged, FanoutExchange fileStagedExchange) {
        return BindingBuilder.bind(queueFileStaged).to(fileStagedExchange);
    }

    @Bean Binding bindingFile(Queue queueFileUpdate, FanoutExchange fileExchange) {
        return BindingBuilder.bind(queueFileUpdate).to(fileExchange);
    }

    @Bean Binding bindingSubmission(Queue queueEnvelopeSubmitted,
                                    FanoutExchange envelopeExchange) {
        return BindingBuilder.bind(queueEnvelopeSubmitted)
                .to(envelopeExchange);
    }

    @Bean Binding bindingValidation(Queue queueValidationRequired, FanoutExchange validationExchange) {
        return BindingBuilder.bind(queueValidationRequired).to(validationExchange);
    }

    /* rabbit config */

    @Bean
    public MessageConverter messageConverter() {
        return jackson2Converter();
    }

    @Bean
    public MappingJackson2MessageConverter jackson2Converter() {
       ObjectMapper mapper = new ObjectMapper();

       mapper.registerModule(new JavaTimeModule());
       mapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);

       return new MappingJackson2MessageConverter();
    }

    @Bean
    public DefaultMessageHandlerMethodFactory myHandlerMethodFactory() {
        DefaultMessageHandlerMethodFactory factory = new DefaultMessageHandlerMethodFactory();
        factory.setMessageConverter(jackson2Converter());
        return factory;
    }

    @Bean
    public RabbitMessagingTemplate rabbitMessagingTemplate(RabbitTemplate rabbitTemplate) {
        RabbitMessagingTemplate rmt = new RabbitMessagingTemplate(rabbitTemplate);
        rmt.setMessageConverter(this.jackson2Converter());
        return rmt;
    }


    @Override
    public void configureRabbitListeners(RabbitListenerEndpointRegistrar registrar) {
        registrar.setMessageHandlerMethodFactory(myHandlerMethodFactory());
    }
}
