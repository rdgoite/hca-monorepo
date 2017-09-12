package org.humancellatlas.ingest.submission;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import org.humancellatlas.ingest.core.AbstractEntity;
import org.humancellatlas.ingest.core.EntityType;
import org.humancellatlas.ingest.core.Event;
import org.humancellatlas.ingest.core.MetadataDocument;
import org.humancellatlas.ingest.core.SubmissionDate;
import org.humancellatlas.ingest.core.UpdateDate;
import org.humancellatlas.ingest.core.Uuid;
import org.humancellatlas.ingest.core.ValidationState;
import org.humancellatlas.ingest.core.exception.MetadataDocumentStateException;
import org.humancellatlas.ingest.submission.state.InvalidSubmissionStateException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Javadocs go here!
 *
 * @author Tony Burdett
 * @date 30/08/17
 */
@Getter
public class SubmissionEnvelope extends AbstractEntity {
    private final List<Event> events;

    private final @JsonIgnore Map<String, ValidationState> validationStateMap;

    private SubmissionState submissionState;

    private static final Logger log = LoggerFactory.getLogger(SubmissionEnvelope.class);

    private static Logger getLog() {
        return log;
    }

    public SubmissionEnvelope(Uuid uuid,
                              SubmissionDate submissionDate,
                              UpdateDate updateDate,
                              SubmissionState submissionState) {
        super(EntityType.SUBMISSION, uuid, submissionDate, updateDate);
        this.events = new ArrayList<>();
        this.validationStateMap = new HashMap<>();
        this.submissionState = submissionState;
    }

    public SubmissionEnvelope() {
        this(null,
             new SubmissionDate(new Date()),
             new UpdateDate(new Date()),
             SubmissionState.DRAFT);
    }

    public static List<SubmissionState> allowedStateTransitions(SubmissionState fromState) {
        List<SubmissionState> allowedStates = new ArrayList<>();
        switch (fromState) {
            case PENDING:
                allowedStates.add(SubmissionState.DRAFT);
                break;
            case DRAFT:
                allowedStates.add(SubmissionState.VALIDATING);
                break;
            case VALIDATING:
                allowedStates.add(SubmissionState.VALID);
                allowedStates.add(SubmissionState.INVALID);
                break;
            case VALID:
                allowedStates.add(SubmissionState.DRAFT);
                allowedStates.add(SubmissionState.SUBMITTED);
                break;
            case INVALID:
                allowedStates.add(SubmissionState.DRAFT);
                allowedStates.add(SubmissionState.VALIDATING);
                break;
            case SUBMITTED:
                allowedStates.add(SubmissionState.PROCESSING);
                break;
            case PROCESSING:
                allowedStates.add(SubmissionState.CLEANUP);
                break;
            case CLEANUP:
                allowedStates.add(SubmissionState.COMPLETE);
                break;
            default:
                getLog().warn(String.format("There are no legal state transitions for '%s' state", fromState.name()));
                break;
        }
        return allowedStates;
    }

    public List<SubmissionState> allowedStateTransitions() {
        return allowedStateTransitions(getSubmissionState());
    }

    public SubmissionEnvelope addEvent(Event event) {
        this.events.add(event);

        return this;
    }

    public SubmissionEnvelope enactStateTransition(SubmissionState targetState) {
        if (!allowedStateTransitions().contains(targetState)) {
            throw new InvalidSubmissionStateException(String.format("The submission state '%s' is not recognised " +
                                                                            "as a submission envelope state that can be set",
                                                                    submissionState.name()));
        }
        this.submissionState = targetState;

        return this;
    }

    public SubmissionEnvelope notifyOfMetadataDocumentState(MetadataDocument metadataDocument) {
        if (!isTrackingMetadata(metadataDocument)) {
            // if this doc is pending, it's either a new document or has new content, so it's ok to add to state tracker
            // but if not, we need to throw an exception here
            if (!metadataDocument.getValidationState().equals(ValidationState.PENDING)) {
                throw new MetadataDocumentStateException(String.format(
                        "Metadata document '%s' was not being tracked by containing envelope '%s' and does not have new content",
                        metadataDocument,
                        this));
            }
        }
        this.validationStateMap.put(metadataDocument.getId(), metadataDocument.getValidationState());

        return this;
    }

    public SubmissionState determineEnvelopeState() {
        final Iterator<Map.Entry<String, ValidationState>> validationStateMapIterator =
                validationStateMap.entrySet().iterator();

        boolean isSomethingValidating = false;
        boolean isSomethingInvalid = false;

        while (validationStateMapIterator.hasNext()) {
            Map.Entry<String, ValidationState> entry = validationStateMapIterator.next();
            ValidationState nextTrackedDocumentState = entry.getValue();

            switch (nextTrackedDocumentState) {
                case VALIDATING:
                    // this document is validating, so we can set the envelope state to validating (as long as nothing is invalid)
                    isSomethingValidating = true;
                    break;
                case VALID:
                    // this document has finished validating, we can remove it from the map
                    validationStateMapIterator.remove();
                    break;
                case INVALID:
                    // if the envelope is already invalid, we can continue cleaning up...
                    isSomethingInvalid = true;
                    // but if the envelope is not invalid, we need to flag the state change
                    if (!getSubmissionState().equals(SubmissionState.INVALID)) {
                        // need to mark as invalid immediately
                        return SubmissionState.INVALID;
                    }
            }
        }

        // decision time!
        // according to spec...
        //     - if >=1 metadata documents are invalid, the envelope is invalid
        //     - otherwise, if >=1 metadata documents are validating, then the envelope is validating
        //     - if everything is now valid (state > PENDING and nothing in the validationStateMap) the envelope is valid
        //     - otherwise, nothing changes

        if (isSomethingInvalid) {
            return SubmissionState.INVALID;
        }
        if (isSomethingValidating) {
            return SubmissionState.VALIDATING;
        }
        if (hasReceivedDocuments() && !isTrackingMetadata()) {
            return SubmissionState.VALID;
        }

        return getSubmissionState();
    }

    public boolean hasReceivedDocuments() {
        return getSubmissionState().compareTo(SubmissionState.PENDING) > 0;
    }

    public boolean isTrackingMetadata() {
        return validationStateMap.size() > 0;
    }

    public boolean isTrackingMetadata(MetadataDocument metadataDocument) {
        return validationStateMap.containsKey(metadataDocument.getId());
    }
}
